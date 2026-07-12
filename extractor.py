import json
from pathlib import Path
import hashlib
from PIL import Image
import numpy as np

from data_types import ChartData, PalaceData, StarData



DOWNLOAD_DIR = Path("downloads"); DOWNLOAD_DIR.mkdir(exist_ok=True)
STAR_DATA_DIR = Path("star_data"); STAR_DATA_DIR.mkdir(exist_ok=True)
STAR_IMAGES_DIR = STAR_DATA_DIR / Path("star_images"); STAR_IMAGES_DIR.mkdir(exist_ok=True)
HASH_IMAGES_DIR = STAR_DATA_DIR / Path("hash_images"); HASH_IMAGES_DIR.mkdir(exist_ok=True)
CHART_IMAGES_DIR = STAR_DATA_DIR / Path("chart_images"); CHART_IMAGES_DIR.mkdir(exist_ok=True)


EMPTY_HASHES = set([
    'f0504c142fa8dfa7c0351fd7d8db19ea0d151be6d088e81dd20107805997581e',
])


with open('hash_data.json', encoding='utf-8') as f:
    hashes_data = json.load(f)


# Get next chart index
chart_index = -1
for f in STAR_IMAGES_DIR.glob("s*.png"):
    try:
        chart_index = max(chart_index, int(f.stem[1:]))
    except:
        pass
chart_index += 1



def load_image(path: Path | str):
    return Image.open(path)

def get_next_free_star_id():
    global hashes_data
    star_id = -1
    for v in hashes_data.values():
        if v['id'] > star_id:
            star_id = v['id']
    return star_id + 1

def iter_palaces_start_pos():
    for iy, y in enumerate((11, 487, 963, 1439)):
        for ix, x in enumerate((14, 370, 724, 1084)):
            # Skip the middle slots which are not palaces
            if ix in (1, 2) and iy in (1, 2):
                continue
            yield (x, y)

def iter_star_column_crop_area(start_x, start_y, width, height, step, max_count):
    '''
    This function increment `start_pos` by `height` to obtain next start pos
    '''
    for i in range(max_count):
        yield (start_x, start_y+step*i, start_x+width, start_y+height+step*i)

def crop_and_get_star_hash(image_arr, crop_area, is_fill_crop_area=False):
    left, top, right, bottom = crop_area
    cropped_image = image_arr[top:bottom:2, left:right:2]
    if is_fill_crop_area:
        cropped_image[6:, 50:] = (253, 204, 204)
    star_hash = hashlib.sha256(cropped_image.tobytes()).hexdigest()

    # # Debug
    # Image.fromarray(cropped_image).save('cropped_result.png')
    # print(star_hash)
    # input()

    return star_hash

def is_chart_valid(image_arr):
    '''
    Chart sometimes have render issues in it lmao
    We use this to filter out unusable charts
    '''

    # Issue #1, column contain too many stars to the point of overlapping posibility
    for psx, psy in iter_palaces_start_pos():
        # left col
        if not np.all(image_arr[psy+436, psx+6:psx+26] == (253, 250, 250)):
            return False
        
        # right col
        if not np.all(image_arr[psy+404, psx+192:psx+211] == (253, 250, 250)):
            return False
        
    # Issue #2, float precision being ahh for the "Cân xương tính số" part (lol)
    if not np.all(image_arr[1142, 1085:1099] == (253, 250, 250)):
        return False
    
    return True



def archive_new_star(image_arr, star:StarData, star_hash, crop_area):
    global chart_index

    left, top, right, bottom = crop_area

    star_image = image_arr[top-10:bottom+10, left-30:right+30]
    star_image_path = STAR_IMAGES_DIR / f"s{chart_index:06d}.png"
    Image.fromarray(star_image).save(star_image_path)

    hash_image = image_arr[top:bottom:2, left:right:2]
    hash_image_path = HASH_IMAGES_DIR / f"h{chart_index:06d}.png"
    Image.fromarray(hash_image).save(hash_image_path)

    chart_image_path = CHART_IMAGES_DIR / f"c{chart_index:06d}.png"
    Image.fromarray(image_arr).save(chart_image_path)

    hashes_data[star_hash] = {
        'name' : None,
        'image' : str(star_image_path),
        'hash_image' : str(hash_image_path),
        'chart_image' : str(chart_image_path),
        'id' : star.id
    }

    with open('hash_data.json', 'w', encoding='utf-8') as f:
        json.dump(hashes_data, f, indent=4, ensure_ascii=False)
    
    chart_index += 1

def process_left_col(image_arr, psx, psy):
    sx = psx + 27
    sy = psy + 127

    stars = []
    for crop_area in iter_star_column_crop_area(sx, sy, 123, 26, 30, 10):
        star_hash = crop_and_get_star_hash(image_arr, crop_area, True)
        if star_hash in EMPTY_HASHES:
            break
        if star_hash not in hashes_data:
            star = StarData(get_next_free_star_id())
            archive_new_star(image_arr, star, star_hash, crop_area)
        else:
            star = StarData(hashes_data[star_hash]['id'])
        stars.append(star)
            
    return stars

def process_right_col(image_arr, psx, psy):
    sx = psx + 215
    sy = psy + 129

    stars = []
    for crop_area in iter_star_column_crop_area(sx, sy, 123, 26, 30, 10):
        star_hash = crop_and_get_star_hash(image_arr, crop_area, True)
        if star_hash in EMPTY_HASHES:
            break
        if star_hash not in hashes_data:
            star = StarData(get_next_free_star_id())
            archive_new_star(image_arr, star, star_hash, crop_area)
        else:
            star = StarData(hashes_data[star_hash]['id'])
        stars.append(star)

    return stars

def process_major(image_arr, psx, psy):
    stars = []
    for i in range(2):
        # Find start pos (catches the top of the last close bracket)
        y = psy+62 + 32*i
        for x in range(psx+281, psx+215-1, -1):
            blue_pixel = image_arr[y, x, 2]
            if blue_pixel != 250:
                break
        else:
            return stars

        while True:
            # Sand fall simulation thing cuz lol
            blue_pixel = image_arr[y, x, 2]
            if blue_pixel != 250:
                y -= 1
                continue
            # Reached the top
            if image_arr[y, x-1, 2] == 250:
                break
            x -= 1
        
        # Crop and hash
        sx = x - 98
        sy = y - 3

        crop_area = (sx, sy, sx+99, sy+28)
        star_hash = crop_and_get_star_hash(image_arr, crop_area, True)
        if star_hash in EMPTY_HASHES:
            break
        if star_hash not in hashes_data:
            star = StarData(get_next_free_star_id())
            archive_new_star(image_arr, star, star_hash, crop_area)
        else:
            star = StarData(hashes_data[star_hash]['id'])
        stars.append(star)

    return stars


def process_image(image: Image.Image) -> ChartData | None:
    '''
    palace indices:
    
        0   1   2   3
        
        4           5

        6           7
        
        8   9  10  11
    
    '''

    # Pre-bake the image as an numpy array
    image_arr = np.array(image)

    if not is_chart_valid(image_arr):
        return None

    palaces = []
    for index, (psx, psy) in enumerate(iter_palaces_start_pos()):

        # Process left column stars
        left_stars =  process_left_col(image_arr, psx, psy)

        # Process right column stars
        right_stars = process_right_col(image_arr, psx, psy)

        # Process major stars
        major_stars = process_major(image_arr, psx, psy)

        palace = PalaceData(major_stars, left_stars, right_stars)
        palaces.append(palace)
    
    chart = ChartData(palaces)
    return chart


if __name__ == '__main__':
    IMG_PATH = DOWNLOAD_DIR / 'c000000.png'
    image = load_image(IMG_PATH)
    chart = process_image(image)
    for p in chart.palaces:
        print(
            len(p.major_stars),
            len(p.left_stars),
            len(p.right_stars),
        )






    # for sx, sy in iter_palaces_start_pos():
    #     crop_area = (sx, sy, sx+358, sy+479)
    #     cropped_image = image.crop(crop_area)
    #     cropped_image.save('cropped_result.png')
    #     input('jio')
