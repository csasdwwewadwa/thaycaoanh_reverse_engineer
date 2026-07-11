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
    'f2ee37924268fee2a886e945acb532060457bca695e9c7d5c0a24dca07ef3a7e',
])


with open('hash_data.json') as f:
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

def iter_palaces_start_pos():
    # start_x, start_y = 14, 11
    # dx = (0, 356, 354, 360)
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

def hash_and_crop_star(image_arr, crop_area, is_fill_crop_area=False):
    left, top, right, bottom = crop_area
    cropped_image = image_arr[top:bottom:2, left:right:2]
    if is_fill_crop_area:
        cropped_image[6:, 50:] = (253, 204, 204)
    hashed_image = hashlib.sha256(cropped_image.tobytes()).hexdigest()
        
    star = StarData(hashed_image)

    # Debug

    # Image.fromarray(cropped_image).save('cropped_result.png')
    # print(hashed_image)
    # input()
    return star

def archive_new_star(image_arr, star, crop_area):
    global chart_index

    left, top, right, bottom = crop_area

    star_image = image_arr[top-10:bottom+10, left-30:right+30]
    star_image_path = STAR_IMAGES_DIR / f"s{chart_index:06d}.png"
    Image.fromarray(star_image).save(star_image_path)

    hash_image = image_arr[top:bottom, left:right]
    hash_image_path = HASH_IMAGES_DIR / f"h{chart_index:06d}.png"
    Image.fromarray(hash_image).save(hash_image_path)

    chart_image_path = CHART_IMAGES_DIR / f"h{chart_index:06d}.png"
    Image.fromarray(image_arr).save(chart_image_path)

    hashes_data[star.hash] = {
        'name' : None,
        'image' : str(star_image_path),
        'hash_image' : str(hash_image_path),
        'chart_image' : str(chart_image_path)
    }

    with open('hash_data.json', 'w') as f:
        json.dump(hashes_data, f, indent=4)
    
    chart_index += 1

def process_left_col(image_arr, psx, psy):
    sx = psx + 27
    sy = psy + 127

    stars = []
    for crop_area in iter_star_column_crop_area(sx, sy, 133, 26, 30, 10):
        star = hash_and_crop_star(image_arr, crop_area, True)
        if star.hash in EMPTY_HASHES:
            break
        stars.append(star)
        if star.hash not in hashes_data:
            archive_new_star(image_arr, star, crop_area)
            
    return stars

def process_right_col(image_arr, psx, psy):
    sx = psx + 215
    sy = psy + 129

    stars = []
    for crop_area in iter_star_column_crop_area(sx, sy, 133, 26, 30, 10):
        star = hash_and_crop_star(image_arr, crop_area, True)
        if star.hash in EMPTY_HASHES:
            break
        stars.append(star)
        if star.hash not in hashes_data:
            archive_new_star(image_arr, star, crop_area)

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
        star = hash_and_crop_star(image_arr, crop_area)
        stars.append(star)
        if star.hash not in hashes_data:
            archive_new_star(image_arr, star, crop_area)

    return stars


def process_image(image: Image.Image) -> ChartData:
    '''
    palace indices:
    
        0   1   2   3
        
        4           5

        6           7
        
        8   9  10  11
    
    '''

    # Pre-bake the image as an numpy array
    image_arr = np.array(image)

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
