import torch
from torch.utils.data import DataLoader, IterableDataset
import json
import numpy as np


class PartitionedStreamDataset(IterableDataset):
    """
    Wraps the main streaming dataset and assigns rows to train or val partitions
    on-the-fly to guarantee an exact 80/20 train/val split.
    """
    def __init__(self, filepath='metadata copy.jsonl', mode='train'):
        super().__init__()
        self.base_dataset = StreamModuloDataset(filepath)
        self.mode = mode

    def __iter__(self):
        for i, (inp, out) in enumerate(self.base_dataset):
            is_val = (i % 5 == 0)  # Exactly 20% of the rows map here
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