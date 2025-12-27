import numpy as np
import easyocr
import cv2

reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(image):

    #resize
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    #convert to gray scales
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    #thresholding to pure black and white
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]

    #filter to find horizontal figures
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))

    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

    #delete those from the original image
    cnts, _ = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 3) #painting the lines

    return image

def extract_text_from_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    processed_img = preprocess_image(image)

    results = reader.readtext(
        processed_img,
        allowlist='0123456789',
        detail=1,
        mag_ratio=1.5,
        paragraph=False
    )
    only_text = [res[1] for res in results]
    return '\n'.join(only_text)

    