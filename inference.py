import os
import json
import numpy as np
import torch
import torch.nn as nn
from model_fsq import HierarchicalFSQNet
from model_bigmlp import BigMLP

with open('hash_data.json', encoding='utf-8') as f:
    hashes_data = json.load(f)

star_names = {}
for v in hashes_data.values():
    star_names[v['id']] = v['name']


def run_pipeline(sex, day, month, year, hour, minute, yearcalc, monthcalc):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Executing inference pipeline on device: {device}")
    print("--------------------------------------------------------------------------------")
    
    raw_inp = [[
        palace_i, sex, day,
        month, year, hour,
        minute, yearcalc, monthcalc,
    ] for palace_i in range(12)]
    x = torch.tensor(raw_inp, dtype=torch.float32, device=device)


    model = BigMLP().to(device)

    # ------------------------------------------------------------------
    # ADDED: LOAD PREVIOUSLY SAVED WEIGHTS
    # ------------------------------------------------------------------
    checkpoint_path = 'best_modulo_model.pt'  # Change to 'checkpoint_latest.pt' if preferred
    start_epoch = 0
    best_perfect_match_accuracy = -1.0

    if os.path.exists(checkpoint_path):
        print(f"--> Found existing checkpoint at '{checkpoint_path}'. Loading weights...")
        checkpoint = torch.load(checkpoint_path, map_location=device)
        
        model.load_state_dict(checkpoint['model_state_dict'])
        
        print(f"--> Weights successfully loaded! Model at Epoch {start_epoch + 1} with previous best accuracy: {best_perfect_match_accuracy:.2f}%")
        print("--------------------------------------------------------------------------------")
    else:
        print("--> No existing checkpoint found. Starting training from scratch.")
        print("--------------------------------------------------------------------------------")

    epoch = start_epoch
    model.eval()
    logits, _ = model(x)

    # logits.to('cpu')

    indices = torch.nonzero(logits > 0).tolist()

    chart = [[] for _ in range(12)]
    for i, v in indices:
        chart[i].append(star_names[v])

    for i, palace in enumerate(chart):
        print(f'\n\n--- Palace {i}')
        print(*palace, sep='\n')

if __name__ == "__main__":
    run_pipeline(1, 12, 3, 1980, 23, 23, 2026, 7)