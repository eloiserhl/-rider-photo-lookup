import os
import json
import easyocr
from PIL import Image

# Configuration
IMAGE_DIR = 'photos/'  # Local folder with rider images
OUTPUT_JSON = 'bib_index.json'  # Output mapping file
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# Prepare index: {bib_number: [list of image paths]}
bib_index = {}

def is_image_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

def detect_bib_numbers(image_path):
    try:
        results = reader.readtext(image_path)
        bibs = []
        for (bbox, text, confidence) in results:
            if confidence < 0.5:
                continue
            cleaned = text.replace(" ", "").strip()
            if cleaned.isdigit() and 1 <= len(cleaned) <= 3:
                bibs.append(cleaned)
        return bibs
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
            bib_index[bib].append(fpath)

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(bib_index, f, indent=2)

    print(f"Bib detection completed. Results saved to {OUTPUT_JSON}")

if __name__ == '__main__':
    main()