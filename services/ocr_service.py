import numpy as np
import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):
    #convert to gray scales
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    #thresholding to pure black and white
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    #filter to find horizontal figures
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))

    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    #delete those from the original image
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2) #painting the lines

    return image

def extract_text_from_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    processed_img = preprocess_image(image)

    results = reader.readtext(
        processed_img,
        allowlist='0123456789-|',
        detail=0,
        paragraph=False
    )
    return '\n'.join(results)