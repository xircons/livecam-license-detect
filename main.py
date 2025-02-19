import cv2
import pytesseract
import numpy as np
import time
import re
from fuzzywuzzy import fuzz

last_saved = {}
SAVE_INTERVAL = 10  # set cooldown

def log_match(license_plate):
    with open('matches_log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"Match Found: {license_plate} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

def save_frame(frame, license_plate):
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    filename = f"matched_{license_plate}.jpg"
    cv2.imwrite(filename, frame)
    print(f"save image as {filename}")

def clean_text(text):
    text = ' '.join(text.split())
    text = re.sub(r'[^ก-๙0-9 ]', '', text)
    return text.strip()

def fuzzy_match(text, log_entries):
    for entry in log_entries:
        ratio = fuzz.partial_ratio(text, entry)
        if ratio > 80:
            return entry
    return None

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    contrast = cv2.convertScaleAbs(gray, alpha=1.5, beta=20)
    blurred = cv2.GaussianBlur(contrast, (5, 5), 0)
    adaptive_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    morph_image = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    custom_config = r'--oem 3 --psm 6'
    detected_text = pytesseract.image_to_string(morph_image, config=custom_config, lang='tha+eng').strip()

    print(f"detected text: {detected_text}")
    license_plate = clean_text(detected_text)

    with open('log.txt', 'r', encoding='utf-8') as file:
        log_entries = [line.strip() for line in file.readlines()]

    matched_plate = fuzzy_match(license_plate, log_entries)

    if matched_plate:
        current_time = time.time()
        last_time = last_saved.get(matched_plate, 0)
        
        if current_time - last_time >= SAVE_INTERVAL:
            print(f"match found: {matched_plate}")
            cv2.putText(frame, "match!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            log_match(matched_plate)
            save_frame(frame, matched_plate)
            last_saved[matched_plate] = current_time  # Update last saved timestamp
        else:
            remaining_time = int(SAVE_INTERVAL - (current_time - last_time))
            print(f"match found: {matched_plate}, countdown: {remaining_time} seconds")
    else:
        print("no match.")

    cv2.imshow("Procees camera", morph_image)
    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()