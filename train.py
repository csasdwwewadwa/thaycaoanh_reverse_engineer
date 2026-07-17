import os
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, IterableDataset
from model_bigmlp_trihead import TriHeadBigMLP
from dataset import StreamModuloDataset, PartitionedStreamDataset


def run_pipeline():
    torch.manual_seed(42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Executing pipeline on device: {device}")
    print("--------------------------------------------------------------------------------")

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
    
    # model = HierarchicalFSQNet(input_dim=162, output_dim=195).to(device)
    model = TriHeadBigMLP().to(device)
    # pos_weight = torch.ones([195], device=device) * 5.0  # Penalize 5x for a wrongly-predicted "1".
    # bce_criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    bce_criterion = nn.BCEWithLogitsLoss()
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingWarmRestarts(
        optimizer, 
        T_0=10,      # Number of iterations for the first restart
        T_mult=2,    # Double the cycle length after each restart (10, 20, 40, 80...)
        eta_min=1e-6 # Minimum learning rate
    )

    # ------------------------------------------------------------------
    # ADDED: LOAD PREVIOUSLY SAVED WEIGHTS
    # ------------------------------------------------------------------
    checkpoint_path = 'checkpoint_latest.pt'  # Change to 'checkpoint_latest.pt' if preferred
    start_epoch = 0
    best_perfect_match_accuracy = -1.0

    if os.path.exists(checkpoint_path):
        print(f"--> Found existing checkpoint at '{checkpoint_path}'. Loading weights...")
        checkpoint = torch.load(checkpoint_path, map_location=device)
        
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint.get('epoch', 0)
        best_perfect_match_accuracy = checkpoint.get('best_accuracy', -1.0)
        
        print(f"--> Weights successfully loaded! Resuming from Epoch {start_epoch + 1} with previous best accuracy: {best_perfect_match_accuracy:.2f}%")
        print("--------------------------------------------------------------------------------")
    else:
        print("--> No existing checkpoint found. Starting training from scratch.")
        print("--------------------------------------------------------------------------------")

    epoch = start_epoch
    
    try:
        while True:
            epoch += 1

            # ------------------------------------------------------------------
            # TRAINING PHASE
            # ------------------------------------------------------------------
            model.train()
            train_loss_accumulator = 0.0
            train_correct_bits = 0
            train_total_bits = 0
            train_batches = 0

            for batch_inputs, batch_targets in train_loader:
                batch_inputs, batch_targets = batch_inputs.to(device), batch_targets.to(device)
                
                optimizer.zero_grad()
                logits, _ = model(batch_inputs)

                classification_loss = bce_criterion(logits, batch_targets)
                
                classification_loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
                optimizer.step()
                
                train_loss_accumulator += classification_loss.item()
                train_batches += 1
                
                predictions = (logits > 0.0).float()
                train_correct_bits += (predictions == batch_targets).sum().item()
                train_total_bits += batch_targets.numel()
                
            # ------------------------------------------------------------------
            # EVALUATION PHASE
            # ------------------------------------------------------------------
            model.eval()
            val_bce_loss = 0.0
            val_correct_bits = 0
            val_total_bits = 0
            val_exact_row_matches = 0
            total_val_samples = 0
            
            with torch.no_grad():
                for batch_inputs, batch_targets in val_loader:
                    batch_inputs, batch_targets = batch_inputs.to(device), batch_targets.to(device)
                    
                    logits, _ = model(batch_inputs)
                    val_bce_loss += bce_criterion(logits, batch_targets).item() * batch_inputs.size(0)
                    
                    predictions = (logits > 0.0).float()
                    
                    val_correct_bits += (predictions == batch_targets).sum().item()
                    val_total_bits += batch_targets.numel()
                    
                    row_matches = (predictions == batch_targets).all(dim=1).sum().item()
                    val_exact_row_matches += row_matches
                    total_val_samples += batch_inputs.size(0)
                    
            average_train_loss = train_loss_accumulator / max(1, train_batches)
            average_val_loss = val_bce_loss / max(1, total_val_samples)
            
            train_soft_accuracy = (train_correct_bits / max(1, train_total_bits)) * 100.0
            val_soft_accuracy = (val_correct_bits / max(1, val_total_bits)) * 100.0
            perfect_match_accuracy = (val_exact_row_matches / max(1, total_val_samples)) * 100.0
            
            current_lr = optimizer.param_groups[0]['lr']
            
            print(f"Epoch {epoch:04d} | "
                  f"Train Loss: {average_train_loss:.4f} (Soft Acc: {train_soft_accuracy:.2f}%) | "
                  f"Val Loss: {average_val_loss:.4f} (Soft Acc: {val_soft_accuracy:.2f}%) | "
                  f"Perfect Match: {perfect_match_accuracy:.2f}% | "
                  f"LR: {current_lr:.6f}")

            # ------------------------------------------------------------------
            # CHECKPOINT SAVING
            # ------------------------------------------------------------------
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'best_accuracy': max(perfect_match_accuracy, best_perfect_match_accuracy)
            }
            torch.save(checkpoint, 'checkpoint_latest.pt')
            
            if perfect_match_accuracy > best_perfect_match_accuracy:
                best_perfect_match_accuracy = perfect_match_accuracy
                torch.save(checkpoint, 'best_modulo_model.pt')
                print(f"  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'")
                
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
                'best_accuracy': best_perfect_match_accuracy
            }, 'checkpoint_interrupted.pt')
            print("Saved current weights to 'checkpoint_interrupted.pt'.")

if __name__ == "__main__":
    run_pipeline()