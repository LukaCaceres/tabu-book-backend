import numpy as np
import easyocr
import cv2

reader = easyocr.Reader(['en'])

def extract_text_from_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = reader.readtext(image, allowlist='0123456789|-/')

    full_text = '\n'.join([res[1] for res in results])

    return full_text