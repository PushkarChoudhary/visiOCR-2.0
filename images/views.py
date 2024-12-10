# images/views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from .models import Image, VisitorPass
from django.core.files.base import ContentFile
from utilities.ocr import extract_text_from_image, detect_card_type, extract_aadhaar_details, extract_pan_details
import base64
from utilities.qr_handler import generate_qr
import pytz
from datetime import datetime, timedelta
from django.utils.timezone import localtime, now
from django.db import IntegrityError
from cryptography.fernet import Fernet
import hashlib
import base64
import os

import cv2
import numpy as np
from imutils.perspective import four_point_transform
import pytesseract
import re
import sys
from utilities.ocr_new import get_extracted_data


# Set Tesseract OCR engine path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        try:
            # Get the uploaded image file from request
            image_data = request.FILES.get('image')
            print(1)
            # Save the image in the database
            img_instance = Image.objects.create(image=image_data)
            image_path = img_instance.image.path
            print(image_path)
            img_name = image_path.split("\\")[-1]
            print(img_name)
            extracted_text = extract_text_from_image(image_path)
            print(2)
            
            # Detect card type and extract relevant details
            card_type = detect_card_type(extracted_text)
            print(3)
            if card_type == "aadhaar":
                # details = extract_aadhaar_details(extracted_text)
                details = get_extracted_data(image_path)
            elif card_type == "pan":
                details = extract_pan_details(extracted_text)
                # details = get_extracted_data(image_path)
            else:
                details = {"error": "Could not determine card type"}
            details['qr_img_name'] = 'qr_' + img_name

            return JsonResponse({
                'message': 'Image uploaded successfully',
                'id': img_instance.id,
                'card_type': card_type,
                'details': details
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Return a 400 response for non-POST requests
    return JsonResponse({'error': 'Invalid request'}, status=400)

def upload_page(request):
    return render(request, 'index.html')  # Use just 'index.html' since it's in the root templates folder



@csrf_exempt
def visiting_pass(request):
    data=request.POST.dict()

    qr_img_name = data.get('qr_img_name', 'default_qr.png')
    text = f"http://127.0.0.1:8000/visiting-pass/{data.get('pass_id', 'NA')}/"
    generate_qr(text, qr_img_name)

    dt = datetime.now(pytz.timezone("Asia/Kolkata"))
    date = dt.strftime("%d/%m/%Y")
    time = dt.strftime("%H:%M")

    uuid = None

    if data.get('PAN Number'):
        uuid = data.get('PAN Number')
    else:
        uuid = data.get('Aadhaar Number')

    print(uuid)

    if not uuid:
        return HttpResponse('<h1>Please provide a valid card. No ID detected. Please try again.</h1>')

    context = {
        'visitor_name': data.get('Name', 'NA'),
        'date_of_birth': data.get('DOB', 'NA'),
        'gender': data.get('Gender', 'NA'),
        'phone_number': data.get('phone', 'NA'),
        'email': data.get('Email', 'NA'),
        'purpose': 'Project Meeting',
        'date': date,
        'time': time,
        'duration': data.get('expire_at', 'NA'),
        'authorized_by': data.get('Authorized By', 'NA'),
        'qr_img_name': qr_img_name,
        'pass_id': data.get('pass_id', 'NA'),
        'expire_at': int(data.get('expire_at')),
        'uuid': uuid,
    }

    # Get encryption key and initialize Fernet
    encryption_key = os.getenv('ENCRYPTION_KEY')
    cipher_suite = Fernet(encryption_key)

    # Hash the input UUID
    hash_object = hashlib.sha256(uuid.encode('utf-8'))
    hashed_uuid = base64.b64encode(hash_object.digest()).decode('utf-8')

    try:
        existing_pass = VisitorPass.objects.get(_encrypted_uuid=hashed_uuid)
        if existing_pass.expire_at.astimezone(pytz.timezone('Asia/Kolkata')) >= localtime(now()):
            existing_visitor_pass = existing_pass.__dict__
            existing_visitor_pass.pop('_state',None)
            existing_visitor_pass.pop('id',None)
            return render(request, 'error.html', existing_visitor_pass) 
        else:
            existing_pass.delete()
    except:
        pass
    
    try:
        visitor_pass = VisitorPass.objects.create(
            visitor_name=context['visitor_name'],
            date_of_birth=context['date_of_birth'],
            gender=context['gender'],
            phone_number=context['phone_number'],
            email=context['email'],
            purpose=context['purpose'],
            date=context['date'],
            time=context['time'],
            duration=context['duration'],
            authorized_by=context['authorized_by'],
            qr_img_name=context['qr_img_name'],
            pass_id=context['pass_id'],   
            expire_at = localtime(now()+timedelta(hours=context['expire_at'])),
            uuid=context['uuid'],
        )
    except:
        return render(request, 'error.html', existing_visitor_pass)
  
    return render(request, 'visiting_pass.html', context)

def get_visiting_pass(request, pass_id):
    try:
        visitor_pass = VisitorPass.objects.get(pass_id=pass_id)
    except: 
        visitor_pass = None
    
    if visitor_pass:
        context = {
        'visitor_name': visitor_pass.visitor_name,
        'date_of_birth': visitor_pass.date_of_birth,
        'gender': visitor_pass.gender,
        'phone_number': visitor_pass.phone_number,
        'email': visitor_pass.email,
        'purpose': visitor_pass.purpose,
        'date': visitor_pass.date,
        'time': visitor_pass.time,
        'duration': visitor_pass.duration,
        'authorized_by': visitor_pass.authorized_by,
        'qr_img_name': visitor_pass.qr_img_name,
        'pass_id': visitor_pass.pass_id,
        'expire_at': localtime(visitor_pass.expire_at).strftime('%d/%m/%Y, %H:%M')
        }

        print(context['expire_at'])

        if visitor_pass.expire_at < datetime.now(pytz.timezone('Asia/Kolkata')):
            return HttpResponse(f'<h1 style="color: red;">Pass with pass id {pass_id} expired at {context['expire_at']}.</h1>')
        else: 
            return render(request, 'visiting_pass.html', context)
    else:
        return HttpResponse(f'<h1>No pass exists for pass id {pass_id}.</h1>')

