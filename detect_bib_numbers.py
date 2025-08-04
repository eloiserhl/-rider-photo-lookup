import os
import json
from paddleocr import PaddleOCR

PHOTOS_DIR = "photos"
OUTPUT_FILE = "bib_index.json"

ocr = PaddleOCR(use_textline_orientation=True, lang='en')

results_dict = {}

for filename in os.listdir(PHOTOS_DIR):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    image_path = os.path.join(PHOTOS_DIR, filename)
    try:
        results = ocr.ocr(image_path)
        for line in results[0]:
            text = line[1][0]
            conf = line[1][1]

            if conf < 0.3:
                continue

            digits = ''.join(filter(str.isdigit, text))
            if not digits or len(digits) > 3:
                continue

            if digits not in results_dict:
                results_dict[digits] = []

            results_dict[digits].append(image_path)

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

with open(OUTPUT_FILE, "w") as f:
    json.dump(results_dict, f, indent=2)

print("Bib detection completed. Results saved to bib_index.json")