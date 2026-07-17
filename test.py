import json

with open('hash_data.json', encoding='utf-8') as f:
    hashes_data = json.load(f)

major = []
transit = []
aux = []
for v in hashes_data.values():
    if v['name'][0] in ['-', '+']:
        major.append(v['id'])
    elif v['name'].startswith('L.') or v['name'].startswith('LN.'):
        transit.append(v['id'])
    else:
        aux.append(v['id'])

print(major, transit, aux, sep='\n')