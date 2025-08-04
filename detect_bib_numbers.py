""
import os
import json
from paddleocr import PaddleOCR
from PIL import Image

# Configuration
IMAGE_DIR = 'photos/'
OUTPUT_JSON = 'bib_index.json'
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
MAX_SIDE = 4000

ocr = PaddleOCR(use_textline_orientation=True, lang='en')
bib_index = {}

def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def resize_image_if_needed(img):
    w, h = img.size
    if max(w, h) > MAX_SIDE:
        if w > h:
            new_w = MAX_SIDE
            new_h = int(h * MAX_SIDE / w)
        else:
            new_h = MAX_SIDE
            new_w = int(w * MAX_SIDE / h)
        return img.resize((new_w, new_h))
    return img

def detect_bib_numbers(image_path):
    try:
        with Image.open(image_path) as img:
            img = resize_image_if_needed(img)
            img = img.convert('RGB')
            results = ocr.ocr(img)

        bibs = set()
        for line in results[0]:
            text, confidence = line[1][0], line[1][1]
            cleaned = text.replace(" ", "").strip()
            if confidence >= 0.4 and cleaned.isdigit() and 2 <= len(cleaned) <= 3:
                bibs.add(cleaned)
        return list(bibs)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return []

def main():
    for fname in os.listdir(IMAGE_DIR):
        if not is_image_file(fname):
            continue

        fpath = os.path.join(IMAGE_DIR, fname)
        bibs = detect_bib_numbers(fpath)

        for bib in bibs:
            if bib not in bib_index:
                bib_index[bib] = []
            if fpath not in bib_index[bib]:
                bib_index[bib].append(fpath)

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(bib_index, f, indent=2)

    print(f"Bib detection completed. Results saved to {OUTPUT_JSON}")

if __name__ == '__main__':
    main()
