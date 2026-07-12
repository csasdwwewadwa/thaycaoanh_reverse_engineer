import re
import sys
import time
import random
import threading
import urllib.parse
import json
from pathlib import Path
from queue import Queue
import calendar
import io

import requests
from requests.adapters import HTTPAdapter
from PIL import Image

from chart_extractor import process_image


URL = "https://tuvi.thaycaoanh.net/index.php"
LOG_FILE = "metadata.jsonl"

NUM_DOWNLOADERS = 4
NUM_WRITERS = 1
QUEUE_SIZE = 128

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

IMG_RE = re.compile(r'<img[^>]+src="([^"]+)"', re.I)

thread_local = threading.local()
stop_event = threading.Event()

save_queue = Queue(maxsize=QUEUE_SIZE)

counter_lock = threading.Lock()
status_lock = threading.Lock()
log_lock = threading.Lock()  # Prevents concurrent file writes

downloaded = 0
saved = 0
errors = 0
chart_index = 0
start_time = time.perf_counter()

def get_session():
    if not hasattr(thread_local, "session"):
        s = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=NUM_DOWNLOADERS,
            pool_maxsize=NUM_DOWNLOADERS,
        )
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        s.headers.update(headers)
        thread_local.session = s
    return thread_local.session

def random_form():
<<<<<<< HEAD
    # Pick the year and month first so we know the limits
=======
    # 1. Pick the year and month first so we know the limits
>>>>>>> 62cf3cfa4833c31dc1f50c41442b2df6bcf64853
    year_val = random.randint(1800, 2199)
    month_val = random.randint(1, 12)
    
    # Get the correct maximum number of days for that specific month and year
    _, num_days = calendar.monthrange(year_val, month_val)
    day_val = random.randint(1, num_days)
    
    return {
        "name": "",
        "sex": str(random.choice((1, 2))),
        "day": str(day_val),
        "month": str(month_val),
        "year": str(year_val),
        "caltype": "1",
        "hour": str(random.randint(0, 23)),
        "minute": str(random.randint(0, 59)),
        "yearcalc": str(random.randint(1800, 2199)),
        "monthcalc": str(random.randint(1, 12)),
        "timezone": "235",
        "timezoneOption": "1",
        "solasocanlap": "1",
        "tuychonthangnhuan": "1",
        "submitted": "TRUE",
        "submitcolor": "Lập lá số màu",
    }

def next_chart_index():
    global chart_index
    with counter_lock:
        idx = chart_index
        chart_index += 1
        return idx

def download_chart():
    session = get_session()
    data = random_form()
    r = session.post(URL, data=data, timeout=30)
    r.raise_for_status()

    matches = IMG_RE.findall(r.text)
    image_url = None
    for src in matches:
        full = urllib.parse.urljoin(URL, src)
        if any(x in full.lower() for x in ["laso", "cache", "temp"]):
            image_url = full
            break
    
    if image_url is None:
        image_url = urllib.parse.urljoin(URL, matches[0]) if matches else None
        if not image_url: raise RuntimeError("No image found.")

    r = session.get(image_url, timeout=30)
    r.raise_for_status()
    
    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    return img, data

def downloader():
    global downloaded, errors
    while not stop_event.is_set():
        try:
            img, data = download_chart()
            idx = next_chart_index()
            save_queue.put((idx, img, data))
            with status_lock: downloaded += 1
        except Exception:
            with status_lock: errors += 1

def writer():
    global saved
    while not stop_event.is_set():
        idx, img, data = save_queue.get()
        
        try:
            chart_data = process_image(img)
            
            if chart_data:
                new_item = {
                    "input_data": data,
                    "output_chart": chart_data.to_dict()
                }
                
                with log_lock:
                    with open(LOG_FILE, "a", encoding="utf-8") as outfile:
                        outfile.write(json.dumps(new_item, ensure_ascii=False) + '\n')
                        
        except Exception as e:
            print(f"\nError processing index {idx}: {e}")
            
        finally:
            with status_lock: saved += 1
            save_queue.task_done()


def status_thread():
    while not stop_event.is_set():
        with status_lock:
            d = downloaded
            s = saved
            e = errors

        elapsed = max(time.perf_counter() - start_time, 1e-6)

        sys.stdout.write(
            "\r"
            f"Downloaded: {d:,} | "
            f"Processed: {s:,} | "
            f"Errors: {e:,} | "
            f"Speed: {d / elapsed:.2f}/s | "
            f"Queue: {save_queue.qsize()}/{QUEUE_SIZE}"
        )

        sys.stdout.flush()
        time.sleep(0.2)


if __name__ == "__main__":
    chart_index = 0

    threading.Thread(target=status_thread, daemon=True).start()

    for _ in range(NUM_WRITERS):
        threading.Thread(target=writer, daemon=True).start()

    for _ in range(NUM_DOWNLOADERS):
        threading.Thread(target=downloader, daemon=True).start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_event.set()
        print("\nStopping...")