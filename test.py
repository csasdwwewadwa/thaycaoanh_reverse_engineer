import json
from data_types import *
from tqdm import tqdm

unique_hashes = set()

with open('new_metadata.jsonl') as f:
    for line in tqdm(f):
        if not line.strip():
            continue

        chart = ChartData.from_dict(json.loads(line)['output_chart'])
        for palace in chart.palaces:
            for star in palace.left_stars + palace.right_stars + palace.major_stars:
                unique_hashes.add(star.hash)

print(len(unique_hashes))