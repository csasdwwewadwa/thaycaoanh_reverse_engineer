import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import IterableDataset, DataLoader
import numpy as np
from tqdm import tqdm
import json
import os

from model import SineVQModuloNet


# DATASET PIPELINE

# STREAMING SET: Define two distinct streams using index boundaries 
# to maintain a 80% train / 20% validation split ratio.
class PartitionedStreamDataset(torch.utils.data.IterableDataset):
    def __init__(self, filepath='metadata copy.jsonl', mode='train'):
        super().__init__()
        self.base_dataset = StreamModuloDataset(filepath)
        self.mode = mode

    def __iter__(self):
        for i, (inp, out) in enumerate(self.base_dataset):
            # 80/20 distribution calculation on index tracking numbers
            is_val = (i % 5 == 0)  # 20% of dataset rows match this condition
            if self.mode == 'val' and is_val:
                yield inp, out
            elif self.mode == 'train' and not is_val:
                yield inp, out


class StreamModuloDataset(IterableDataset):
    def __init__(self, filepath='metadata copy.jsonl'):
        super().__init__()
        self.filepath = filepath
        self.frequencies = np.array([2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 17.0, 19.0, 31.0], dtype=np.float32)

    def __iter__(self):
        # Multi-worker safety assignment
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:
            # Single-process data loading (no change)
            worker_id = 0
            num_workers = 1
        else:
            # Split lines across distinct worker IDs
            worker_id = worker_info.id
            num_workers = worker_info.num_workers

        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f):
                # Ensure each worker only processes its assigned lines
                if i % num_workers != worker_id:
                    continue
                    
                if not line.strip():
                    continue
                
                data = json.loads(line)
                input_data = data['input_data']

                for palace_i, palace in enumerate(data['output_chart']['palaces']):
                    raw_inp = [
                        palace_i, int(input_data['sex']), int(input_data['day']),
                        int(input_data['month']), int(input_data['year']), int(input_data['hour']),
                        int(input_data['minute']), int(input_data['yearcalc']), int(input_data['monthcalc']),
                    ]
                    
                    inp_arr = np.array(raw_inp, dtype=np.float32)
                    scaled_matrix = inp_arr[:, np.newaxis] * self.frequencies[np.newaxis, :]
                    
                    sin_features = np.sin(scaled_matrix).flatten()
                    cos_features = np.cos(scaled_matrix).flatten()
                    processed_inp = np.concatenate([sin_features, cos_features])

                    stars = palace["major_stars"] + palace["left_stars"] + palace["right_stars"]
                    out = np.zeros(195, dtype=np.float32)
                    for v in stars:
                        out[v] = 1.0
                
                    yield torch.tensor(processed_inp, dtype=torch.float32), torch.tensor(out, dtype=torch.float32)



# MAIN PIPELINE


def run_pipeline():
    # Set seed for reproducible results
    torch.manual_seed(42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Executing pipeline on device: {device}")
    print("Initializing dataset..")
    
    # DATA LOADERS: Instantiated using the on-the-fly partition streams
    train_dataset = PartitionedStreamDataset(mode='train')
    val_dataset = PartitionedStreamDataset(mode='val')
    
    # Use 4 parallel worker processes to parse JSON text and math arrays simultaneously
    # prefetch_factor=2 keeps 2 batches per worker waiting in RAM ready to instantly swap to GPU
    train_loader = DataLoader(
        train_dataset, 
        batch_size=128, 
        drop_last=True, 
        num_workers=4, 
        prefetch_factor=2,
        pin_memory=True  # Fast-tracks tensor transfers from RAM straight to GPU memory
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=256, 
        num_workers=4,
        prefetch_factor=2,
        pin_memory=True
    )
    
    # Init
    print('Initializing model..')
    model = SineVQModuloNet(output_dim=195, latent_dim=128, num_codes=256).to(device)
    bce_criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, 
        mode='min',      # Minimize val loss
        factor=0.1,      # Cut LR by 10x
        patience=15,     # Wait 15 epochs of no improvement before cutting
    )


    print("--------------------------------------------------------------------------------")

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
                total_loss = classification_loss + vq_loss

                total_loss.backward()
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
                  f"Val Loss: {average_val_loss:.4f} | Perfect Match Accuracy: {perfect_match_accuracy:.2f}% "
                  f"Learning Rate: {optimizer.param_groups[0]['lr']}")
            

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