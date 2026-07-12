import json
from tqdm import tqdm
import os





def load_dataset(filepath):
    """
    Loads pairs from the jsonl file.
    """
    inputs = []
    outputs = []
    
    file_size = os.path.getsize(filepath)
    with open(filepath, 'r') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Processing input file") as pbar:
            for line in f:
                data = json.loads(line)

                input_data = data['input_data']

                for palace_i, palace in enumerate(data['output_chart']['palaces']):
                    inp = [
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
                    out = [
                        palace["major_stars"] + palace["left_stars"] + palace["right_stars"]
                    ]
                
                    inputs.append(inp)
                    outputs.append(out)

                pbar.update(len(line))
                    
    return inputs, outputs

# --- Main Execution Execution ---
if __name__ == "__main__":
    DATASET_PATH = "metadata copy.jsonl"
    
    inputs, outputs = load_dataset(DATASET_PATH)

    print(len(inputs))
    