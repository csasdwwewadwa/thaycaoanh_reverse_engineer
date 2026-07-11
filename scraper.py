import re
import sys
import time
import random
import threading
import urllib.parse
import json  # Added
from pathlib import Path
from queue import Queue

import cv2
import numpy as np
import requests
from requests.adapters import HTTPAdapter

URL = "https://tuvi.thaycaoanh.net/index.php"
DOWNLOAD_DIR = Path("downloads")
LOG_FILE = "metadata.jsonl"

NUM_DOWNLOADERS = 4
NUM_WRITERS = 2
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
log_lock = threading.Lock()  # Added to prevent concurrent file writes

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
    return {
        "name": "",
        "sex": str(random.choice((1, 2))),
        "day": str(random.randint(1, 28)),
        "month": str(random.randint(1, 12)),
        "year": str(random.randint(1900, 2099)),
        "caltype": "1",
        "hour": "12",
        "minute": "0",
        "yearcalc": str(random.randint(1900, 2099)),
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

def find_next_chart_index():
    maximum = -1
    for f in DOWNLOAD_DIR.glob("c*.png"):
        try:
            maximum = max(maximum, int(f.stem[1:]))
        except:
            pass
    return maximum + 1

def download_chart():
    session = get_session()
    data = random_form() # Generate data here to pass it through
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
    image = cv2.imdecode(np.frombuffer(r.content, np.uint8), cv2.IMREAD_COLOR)
    if image is None: raise RuntimeError("Decode failed.")
    
    return image, data

def downloader():
    global downloaded, errors
    while not stop_event.is_set():
        try:
            image, data = download_chart()
            idx = next_chart_index()
            save_queue.put((idx, image, data)) # Pass data to queue
            with status_lock: downloaded += 1
        except Exception:
            with status_lock: errors += 1

def writer():
    global saved
    while not stop_event.is_set():
        idx, image, data = save_queue.get()
        filename = DOWNLOAD_DIR / f"c{idx:06d}.png"
        
        cv2.imwrite(str(filename), image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        
        # Log metadata to JSONL
        entry = {"index": idx, "filename": filename.name, "data": data}
        with log_lock:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")

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
            f"Saved: {s:,} | "
            f"Errors: {e:,} | "
            f"Speed: {d / elapsed:.2f}/s | "
            f"Queue: {save_queue.qsize()}/{QUEUE_SIZE}"
        )

        sys.stdout.flush()

        time.sleep(0.2)


if __name__ == "__main__":
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    chart_index = find_next_chart_index()

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