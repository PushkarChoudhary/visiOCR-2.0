import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
import re
import sys

# Set your Tesseract OCR engine path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class NameLengthException(Exception):
    """Custom exception to handle name length exceeding 15 characters."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def validate_name_length(name_value):
    """Validate the length of the name."""
    if len(name_value) > 15:
        raise NameLengthException(f"Name '{name_value}' exceeds 15 characters. Please verify the correctness of the name.")

def image_processing(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return threshold


def scan_detection(image, frame, width, height):

    global document_contour

    document_contour = np.array([[0, 0], [width, 0], [width, height], [0, height]])

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                document_contour = approx
                max_area = area

    cv2.drawContours(frame, [document_contour], -1, (0, 255, 0), 3)


def extractText(ocr_text):
    aadhaar_match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', ocr_text).group(0)
    dob_value = re.search(r'\b\d{2}/\d{2}/\d{4}\b', ocr_text).group(0)
    gender_value = re.search(r'(Male|Female|MALE|FEMALE)', ocr_text).group(0)
    name_value = re.search(r'\b[A-Z][a-z]*(?:\s+[A-Z][a-z]*){1,3}\b', ocr_text).group(0)

    # Validate name length
    is_invalid_name = False

    try:
        validate_name_length(name_value)
    except NameLengthException as e:
        is_invalid_name = True

    return {
        "is_invalid_name": is_invalid_name,
        "Name": name_value,
        "DOB": dob_value,
        "Gender": gender_value,
        "Aadhaar Number": aadhaar_match if aadhaar_match else "Not found"
    }



def get_extracted_data(image_path):

    frame = cv2.imread(image_path)

    scale = 0.5

    font = cv2.FONT_HERSHEY_SIMPLEX

    HEIGHT, WIDTH, _ = frame.shape

    frame_copy = frame.copy()

    scan_detection(frame_copy, frame, WIDTH, HEIGHT)

    warped = four_point_transform(frame_copy, document_contour.reshape(4, 2))

    processed = image_processing(warped)
    processed = processed[10:processed.shape[0] - 10, 10:processed.shape[1] - 10]

    ocr_text = pytesseract.image_to_string(processed)

    return extractText(ocr_text)


if __name__ == '__main__':
    img_path = r"D:\ocrapi\media\uploads\1732365288446.png"
    get_extracted_data(img_path)
    print(get_extracted_data(img_path))
