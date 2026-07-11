import json
from PIL import Image
import time
from pathlib import Path
from data_types import *
from extractor import process_image, STAR_IMAGES_DIR, HASH_IMAGES_DIR, CHART_IMAGES_DIR
from tqdm import tqdm


def process_chart_data(input_path: str, output_path: str):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in tqdm(infile):
            if not line.strip():
                continue
            
            # 1. Load original metadata
            item = json.loads(line)
            
            # 2. Process image
            try:
                img = Image.open('downloads/' + item["filename"])
                chart_data: ChartData = process_image(img)
            except Exception as e:
                print(f"Error processing {item['filename']}: {e}")
                continue
            
            # 3. Create new structure
            new_item = {
                "index": item["index"],
                "filename": item["filename"],
                "input_data": item["data"],
                "output_chart": chart_data.to_dict()
            }
            
            # 4. Write to new .jsonl
            outfile.write(json.dumps(new_item, ensure_ascii=False) + '\n')


def wipe():
    for f in HASH_IMAGES_DIR.iterdir():
        f.unlink()
    for f in STAR_IMAGES_DIR.iterdir():
        f.unlink()
    for f in CHART_IMAGES_DIR.iterdir():
        f.unlink()
    with open('new_metadata.jsonl', 'w') as f:
        f.write('{}')
    with open('hash_data.json', 'w') as f:
        f.write('{}')

    
if __name__ == '__main__':
    with open('hash_data.json') as f:
        hash_data_text = f.read()

    if hash_data_text.strip() != '{}':
        print('Wiping old data')
        wipe()
        print('Wiped old data! restart to start process chart data.')
    else:
        print('processing chart data')
        process_chart_data('metadata.jsonl', 'new_metadata.jsonl')