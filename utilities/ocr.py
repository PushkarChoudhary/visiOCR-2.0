import re
import pytesseract
from PIL import Image

# Path to custom-trained Tesseract model (if you are using one)
custom_config = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class NameLengthException(Exception):
    """Custom exception to handle name length exceeding 15 characters."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def preprocess_text(text):
    """Clean the extracted text to remove unwanted characters."""
    text = re.sub(r'[^\w\s:/\-]', '', text)  # Remove non-alphanumeric characters except /, :, and -
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

def extract_text_from_image(image_path):
    """Extract text from the image using OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config=custom_config, lang='eng+hin')
    text = preprocess_text(text)
    return text

def validate_name_length(name):
    """Validate the length of the name."""
    if len(name) > 15:
        raise NameLengthException(f"Name '{name}' exceeds 15 characters. Please verify the correctness of the name.")

def detect_card_type(extracted_text):
    card_type = None
    if "Aadhaar" in extracted_text or "आधार" in extracted_text or re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', extracted_text):
        card_type = "aadhaar"
    elif "Income Tax Department" in extracted_text or "Permanent Account Number" in extracted_text or re.search(r'\b[A-Z]{5}\d{4}[A-Z]\b', extracted_text):
        card_type = "pan"
    return card_type
    
    

def extract_aadhaar_details(text):
    """Extract details such as Name, DOB, Gender, and Aadhaar number."""
    name_english_regex = re.compile(r'([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)')  # Capitalized words for name
    dob_regex = re.compile(r'(?i)(?:DOB|D\.O\.B|Date of Birth)\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})')
    gender_regex = re.compile(r'(Male|Female|पुरुष|महिला)', re.IGNORECASE)
    aadhaar_regex = re.compile(r'\b\d{4}\s\d{4}\s\d{4}\b')

    name_match = name_english_regex.search(text)
    dob_match = dob_regex.search(text)
    gender_match = gender_regex.search(text)
    aadhaar_match = aadhaar_regex.search(text)

    gender_map = {"पुरुष": "Male", "महिला": "Female"}
    gender_value = gender_match.group(1) if gender_match else "Not found"
    gender_value = gender_map.get(gender_value, gender_value)
    name_value = name_match.group(1).strip() if name_match else "Not found"
    dob_value = dob_match.group(1) if dob_match else "Not found"

    # Validate name length
    is_invalid_name = False

    try:
        validate_name_length(name_value)
    except NameLengthException as e:
        is_invalid_name = True

        print(e.message)
        # print("Do you still want to proceed with the current name? (Y/y for Yes, N/n for No)")
        # proceed = input("Enter your choice: ").strip().lower()
        # if proceed not in ['y', 'yes']:
        #     print("Exiting as per your choice. Please correct the name and try again.")
        #     exit()

    return {
        "is_invalid_name": is_invalid_name,
        "Name": name_value,
        "DOB": dob_value,
        "Gender": gender_value,
        "Aadhaar Number": aadhaar_match.group(0) if aadhaar_match else "Not found"
        

    }

def extract_pan_details(text):
    """Extract details such as Name, Father's Name, DOB, and PAN number from PAN card."""
    name_regex = re.compile(r'(?<=Name)\s*[:\-]?\s*([A-Z][a-zA-Z\s]+)')
    dob_regex = re.compile(r'(?<=Date of Birth)\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})')
    pan_regex = re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b')

    name_match = name_regex.search(text)
    dob_match = dob_regex.search(text)
    pan_match = pan_regex.search(text)

    name_value = name_match.group(1).strip() if name_match else "Not found"
    dob_value = dob_match.group(1) if dob_match else "Not found"
    pan_value = pan_match.group(0) if pan_match else "Not found"

    # Validate name length
    is_invalid_name = False
    try:
        validate_name_length(name_value)
    except NameLengthException as e:
        is_invalid_name = True
        print(e.message)
        # print("Do you still want to proceed with the current name? (Y/y for Yes, N/n for No)")
        # proceed = input("Enter your choice: ").strip().lower()
        # if proceed not in ['y', 'yes']:
        #     print("Exiting as per your choice. Please correct the name and try again.")
        #     exit()

    return {
        "is_invalid_name": is_invalid_name,
        "Name": name_value,
        "DOB": dob_value,
        "PAN Number": pan_value
    
    }

if __name__ == "__main__":
    # Path to your image (Replace with actual image path)
    image_path = r"D:\ocrapi\test\test_images\aadhaar\aadhar1.jpg"  # Replace with your image path
    # Step 1: Extract the text from the image using OCR
    extracted_text = extract_text_from_image(image_path)
    # Step 2: Extract details from the OCR text if Aadhaar or PAN keywords are detected
    card_type = detect_card_type(extracted_text)

    if card_type == "aadhaar":
        print("Detected Aadhaar Card")
        details = extract_aadhaar_details(extracted_text)
    elif card_type == "pan":
        print("Detected PAN Card")
        details = extract_pan_details(extracted_text)
    else:
        details = {"Error": "Could not determine card type"}

    # Step 3: Print the extracted details
    for key, value in details.items():
        print(f"{key}: {value}")

