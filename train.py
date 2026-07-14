# train.py - With ModuloNetNoVQ and Soft Metric Tracking

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import IterableDataset, DataLoader
import numpy as np
from tqdm import tqdm
import json
import os

from model import ModuloNetNoVQ # <-- Import the updated No-VQ class


# DATASET PIPELINE

class PartitionedStreamDataset(torch.utils.data.IterableDataset):
    def __init__(self, filepath='metadata copy.jsonl', mode='train'):
        super().__init__()
        self.base_dataset = StreamModuloDataset(filepath)
        self.mode = mode

    def __iter__(self):
        for i, (inp, out) in enumerate(self.base_dataset):
            is_val = (i % 5 == 0)  # 20% validation split
            if self.mode == 'val' and is_val:
                yield inp, out
            elif self.mode == 'train' and not is_val:
                yield inp, out


class StreamModuloDataset(IterableDataset):
    def __init__(self, filepath='metadata copy.jsonl'):
        super().__init__()
        self.filepath = filepath

    def __iter__(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:
            worker_id = 0
            num_workers = 1
        else:
            worker_id = worker_info.id
            num_workers = worker_info.num_workers

        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f):
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
                    
                    stars = palace["major_stars"] + palace["left_stars"] + palace["right_stars"]
                    out = np.zeros(195, dtype=np.float32)
                    for v in stars:
                        out[v] = 1.0
                
                    yield torch.tensor(raw_inp, dtype=torch.float32), torch.tensor(out, dtype=torch.float32)


# MAIN PIPELINE

def run_pipeline():
    torch.manual_seed(42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Executing pipeline on device: {device}")

    train_dataset = PartitionedStreamDataset(mode='train')
    val_dataset = PartitionedStreamDataset(mode='val')
    
    train_loader = DataLoader(
        train_dataset, 
        batch_size=128, 
        drop_last=True, 
        num_workers=4, 
        prefetch_factor=2,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=256, 
        num_workers=4,
        prefetch_factor=2,
        pin_memory=True
    )
    
    # Initialize the Continuous No-VQ Model
    base_model = ModuloNetNoVQ(
        in_features=1, 
        latent_dim=512, 
        num_heavy_blocks=2
    )
    
    classification_head = nn.Sequential(
        nn.Flatten(),
        nn.Linear(9 * 512, 195)
    )
    
    model = nn.Sequential(base_model, classification_head).to(device)
    
    bce_criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, 
        mode='min',
        factor=0.1,
        patience=15,
    )

    print("--------------------------------------------------------------------------------")

    epoch = 0
    best_accuracy = -1.0
    
    try:
        while True:
            epoch += 1

            # Training phase
            model.train()
            train_loss_accumulator = 0.0
            train_batches = 0
            train_soft_correct = 0
            train_soft_total = 0

            for batch_inputs, batch_targets in train_loader:
                batch_inputs = batch_inputs.unsqueeze(-1).to(device)
                batch_targets = batch_targets.to(device)
                
                optimizer.zero_grad()
                
                quantized, vq_loss, _ = model[0](batch_inputs)
                logits = model[1](quantized)

                classification_loss = bce_criterion(logits, batch_targets)
                total_loss = classification_loss + vq_loss # vq_loss is 0.0 here

                total_loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
                optimizer.step()
                
                # Calculate training soft accuracy
                train_preds = (logits > 0.0).float()
                train_soft_correct += (train_preds == batch_targets).sum().item()
                train_soft_total += batch_targets.numel()

                train_loss_accumulator += total_loss.item()
                train_batches += 1
                
            # Eval phase
            model.eval()
            val_bce_loss = 0.0
            exact_row_matches = 0
            total_val_samples = 0
            val_soft_correct = 0
            val_soft_total = 0
            
            with torch.no_grad():
                for batch_inputs, batch_targets in val_loader:
                    batch_inputs = batch_inputs.unsqueeze(-1).to(device)
                    batch_targets = batch_targets.to(device)
                    
                    quantized, _, _ = model[0](batch_inputs)
                    logits = model[1](quantized)
                    
                    val_bce_loss += bce_criterion(logits, batch_targets).item() * batch_inputs.size(0)
                    
                    predictions = (logits > 0.0).float()
                    
                    # Soft metric: individual star accuracy
                    val_soft_correct += (predictions == batch_targets).sum().item()
                    val_soft_total += batch_targets.numel()

                    # Hard metric: perfect row matches
                    row_matches = (predictions == batch_targets).all(dim=1).sum().item()
                    exact_row_matches += row_matches
                    total_val_samples += batch_inputs.size(0)
                    
            average_train_loss = train_loss_accumulator / max(1, train_batches)
            average_val_loss = val_bce_loss / max(1, total_val_samples)
            
            train_soft_acc = (train_soft_correct / max(1, train_soft_total)) * 100.0
            val_soft_acc = (val_soft_correct / max(1, val_soft_total)) * 100.0
            perfect_match_accuracy = (exact_row_matches / max(1, total_val_samples)) * 100.0
            
            print(f"Epoch {epoch:04d} | Train Loss: {average_train_loss:.4f} (Soft Acc: {train_soft_acc:.2f}%) | "
                  f"Val Loss: {average_val_loss:.4f} (Soft Acc: {val_soft_acc:.2f}%) | "
                  f"Perfect Match: {perfect_match_accuracy:.2f}% | "
                  f"LR: {optimizer.param_groups[0]['lr']:.6f}")

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
                print(f"  -->  New best perfect match acc! Saved weights to 'best_modulo_model.pt'")
                
                if perfect_match_accuracy == 100.0:
                    print("\nAchieved 100% absolute accuracy! INFERENCE TEST TIME BABYYYYY")
                    break

            scheduler.step(average_val_loss)

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