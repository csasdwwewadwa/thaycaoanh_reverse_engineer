import json
from PIL import Image

with open('hash_data.json', encoding='utf-8') as f:
    data = json.load(f)

keys = list(data.keys())

i = 0
while True:
    k = keys[i]
    v = data[k]

    if v['name'] is not None:
        i += 1
        continue

    image = Image.open(v['image'])
    image.save('cropped_result.png')


    v['name'] = input(f'Star [{v['id']}] name: ')

    if v['name'] == 'u':
        i -= 1
        continue

    if i < len(keys) - 1:
        i += 1
    else:
        print('done')
        quit()
    
    with open('hash_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)