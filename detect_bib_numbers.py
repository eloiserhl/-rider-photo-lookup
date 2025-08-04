import os
import json
from paddleocr import PaddleOCR
from PIL import Image

# Configuration
IMAGE_DIR = 'photos/'  # Local folder with rider images
OUTPUT_JSON = 'bib_index.json'  # Output mapping file
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

# Prepare index: {bib_number: [list of image paths]}
bib_index = {}

def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def detect_bib_numbers(image_path):
    try:
        results = ocr.ocr(image_path, cls=True)
        bibs = set()
        for line in results[0]:
            text, confidence = line[1][0], line[1][1]
            cleaned = text.replace(" ", "").strip()
            if confidence >= 0.5 and cleaned.isdigit() and 2 <= len(cleaned) <= 3:
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