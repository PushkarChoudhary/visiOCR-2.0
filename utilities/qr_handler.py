import pyqrcode 
import png 
from pyqrcode import QRCode 

def generate_qr(text, image_name):
    # Generate QR code 
    url = pyqrcode.create(text) 
    
    # Create and save the png file 
    url.png(f"D:\ocrapi\images\static\qr_codes\\{image_name}", scale = 6)

# Test

if "__name__" == "main":
    # String which represents the QR code 
    text = "www.geeksforgeeks.org"
    image_name = "test_qr.png"

    generate_qr(text, image_name)

