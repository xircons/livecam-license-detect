# Camera License Plate Detection

This project captures license plates from camera, compares them to a log of known plates, and saves images of matched plates with timestamps.

## Features

License plate detection using OpenCV and Tesseract OCR.
Matches detected plates against a log of allowed plates.
Saves images of matched plates.
Fuzzy matching for partial plate matches.

## Requirements

- OpenCV
- Tesseract OCR
- fuzzywuzzy
- numpy

## Files

- `main.py` : Main script to run the program.
- `log.txt` : Database containing allowed license plates.
- `venv` : Python virtual environment with required packages.

This project is still in development, with improvements planned over time. Any feedback or suggestions are welcome!
