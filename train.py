import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
from tqdm import tqdm
import json
import os

from model import SineVQModuloNet


# DATASET PIPELINE

class ModuloDataset(Dataset):
    def __init__(self, inputs_list, outputs_list):
        # inputs_list contains pre-computed 162-dimensional sine/cosine arrays
        self.inputs = torch.tensor(inputs_list, dtype=torch.float32)
        # Outputs must be float32 for BCEWithLogitsLoss target constraints
        self.outputs = torch.tensor(outputs_list, dtype=torch.float32)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs[idx], self.outputs[idx]


def load_dataset(filepath='metadata copy.jsonl'):
    """
    Loads pairs from the jsonl file and pre-computes multi-frequency periodic features.
    """
    inputs = []
    outputs = []
    
    # Setup prime frequencies for preprocessing
    # TODO: other, specific frequencies might be beneficial?
    frequencies = np.array([2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 31.0], dtype=np.float32)
    
    file_size = os.path.getsize(filepath)
    with open(filepath, 'r') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Processing input file") as pbar:
            for line in f:
                data = json.loads(line)
                input_data = data['input_data']

                for palace_i, palace in enumerate(data['output_chart']['palaces']):
                    raw_inp = [
                        palace_i,
                        int(input_data['sex']),
                        int(input_data['day']),
                        int(input_data['month']),
                        int(input_data['year']),
                        int(input_data['hour']),
                        int(input_data['minute']),
                        int(input_data['yearcalc']),
                        int(input_data['monthcalc']),
                    ]
                    
                    inp_arr = np.array(raw_inp, dtype=np.float32)
                    
                    # (9, 9)
                    scaled_matrix = inp_arr[:, np.newaxis] * frequencies[np.newaxis, :]
                    
                    sin_features = np.sin(scaled_matrix).flatten()
                    cos_features = np.cos(scaled_matrix).flatten()
                    
                    # Combine into a final 162-dimensional feature vector
                    processed_inp = np.concatenate([sin_features, cos_features]).tolist()

                    stars = palace["major_stars"] + palace["left_stars"] + palace["right_stars"]
                    out = [0] * 195
                    for v in stars:
                        out[v] = 1
                
                    inputs.append(processed_inp)
                    outputs.append(out)

                pbar.update(len(line))
                    
    return inputs, outputs



# MAIN PIPELINE


def run_pipeline():
    # Set seed for reproducible results
    torch.manual_seed(42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Executing pipeline on device: {device}")
    print("--------------------------------------------------------------------------------")

    # Load data
    raw_inputs, raw_outputs = load_dataset()
    dataset_size = len(raw_inputs)
    
    # Split indices (80% train / 20% val)
    indices = np.arange(dataset_size)
    np.random.shuffle(indices)
    
    val_split_edge = int(dataset_size * 0.2)
    val_indices = indices[:val_split_edge]
    train_indices = indices[val_split_edge:]
    
    train_in = [raw_inputs[i] for i in train_indices]
    train_out = [raw_outputs[i] for i in train_indices]
    val_in = [raw_inputs[i] for i in val_indices]
    val_out = [raw_outputs[i] for i in val_indices]
    
    train_dataset = ModuloDataset(train_in, train_out)
    val_dataset = ModuloDataset(val_in, val_out)
    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_dataset, batch_size=256, shuffle=False)
    
    # Init
    model = SineVQModuloNet(output_dim=195, latent_dim=128, num_codes=256).to(device)
    bce_criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    # Smoothly lowers the learning rate as epochs progress
    # TODO: FIX SUDDEN LOSS SPIKES
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100, eta_min=1e-5)
    



    # Main loop
    epoch = 0
    best_accuracy = -1.0
    
    try:
        while True:
            epoch += 1

            # Training phase
            model.train()
            train_loss_accumulator = 0.0

            for batch_inputs, batch_targets in train_loader:
                batch_inputs, batch_targets = batch_inputs.to(device), batch_targets.to(device)
                
                optimizer.zero_grad()

                logits, vq_loss = model(batch_inputs)
                classification_loss = bce_criterion(logits, batch_targets)

                # VQ Warmup: Keep VQ weight at 0.0 for the first 5 epochs, then slowly scale up
                # NOTE
                if epoch <= 5:
                    vq_weight = 0.0
                else:
                    vq_weight = min(0.02, (epoch - 5) * 0.002) if epoch > 5 else 0.0

                total_loss = classification_loss + (vq_loss * vq_weight)
                
                total_loss.backward()
                
                # Protect against sudden sharp gradient boundaries in the lookup cells
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
                
                optimizer.step()
                
                train_loss_accumulator += total_loss.item()
                
            # Eval phase
            model.eval()
            val_bce_loss = 0.0
            exact_row_matches = 0
            total_val_samples = 0
            
            with torch.no_grad():
                for batch_inputs, batch_targets in val_loader:
                    batch_inputs, batch_targets = batch_inputs.to(device), batch_targets.to(device)
                    
                    logits, _ = model(batch_inputs)
                    val_bce_loss += bce_criterion(logits, batch_targets).item() * batch_inputs.size(0)
                    
                    predictions = (logits > 0.0).float()
                    row_matches = (predictions == batch_targets).all(dim=1).sum().item()
                    exact_row_matches += row_matches
                    total_val_samples += batch_inputs.size(0)
                    
            average_train_loss = train_loss_accumulator / len(train_loader)
            average_val_loss = val_bce_loss / total_val_samples
            perfect_match_accuracy = (exact_row_matches / total_val_samples) * 100.0
            
            print(f"Epoch {epoch:04d} | Train Loss: {average_train_loss:.4f} | "
                  f"Val Loss: {average_val_loss:.4f} | Perfect Match Accuracy: {perfect_match_accuracy:.2f}%")
            

            # Saving phase
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'best_accuracy': max(perfect_match_accuracy, best_accuracy)
            }
            torch.save(checkpoint, 'checkpoint_latest.pt')
            
            if perfect_match_accuracy > best_accuracy:
                best_accuracy = perfect_match_accuracy
                torch.save(checkpoint, 'best_modulo_model.pt')
                print(f"  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'")
                
                if perfect_match_accuracy == 100.0:
                    print("\nAchieved 100% absolute accuracy! INFERENCE TEST TIME BABYYYYY")
                    break

            scheduler.step()

    except KeyboardInterrupt:
        print("\n--------------------------------------------------------------------------------")
        print("Training stopped.")
        
        if epoch > 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'best_accuracy': best_accuracy
            }, 'checkpoint_interrupted.pt')
            print("Saved current weights to 'checkpoint_interrupted.pt'.")


if __name__ == "__main__":
    run_pipeline()