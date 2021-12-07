from paddleocr import PaddleOCR
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
import re

# regex for portuguese license plates
plate_regex = "[0-9]{2}[\s-]{0,1}[0-9]{2}[\s-]{0,1}[A-Z]{2}|" \
              "[0-9]{2}[\s-]{0,1}[A-Z]{2}[\s-]{0,1}[0-9]{2}|" \
              "[A-Z]{2}[\s-]{0,1}[0-9]{2}[\s-]{0,1}[A-Z]{2}"

# Initiate FastAPI and PaddleOCR
app = FastAPI(title="OCR-API", debug=True, version="0.1")
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def format_plate(plate=None):
    # Remove hifens and empty spaces
    plate = plate.replace(' ', '')
    plate = plate.replace('-', '')

    # Format to the following standard licence plate XX-XX-XX
    return plate[:2] + '-' + plate[2:4] + '-' + plate[4:]


def bytes_to_jpg(image=None, camera=None):
    data = np.fromfile(image, dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('plate.jpg', gray)


def ocr_reader(image='plate.jpg', ocr_object=ocr):
    reader = ocr_object.ocr(image)
    results = [i[1][0] for i in reader]  # iterate all the results

    for result in results:
        matched = bool(re.match(plate_regex, result))
        if matched is True:
            print(result)
            return format_plate(result)


@app.post('/files')
async def upload_file(image: UploadFile = File(...)):
    # Convert to numpy 1d array (grayscale)
    bytes_to_jpg(image.file)

    # Predict plate
    plate = ocr_reader()

    return plate
