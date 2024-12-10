# images/models.py
from django.db import models
from django.utils import timezone
import pytz
from cryptography.fernet import Fernet
import hashlib
import base64
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# from encrypted_fields import EncryptedCharField

def get_kolkata_time():
    # Set the timezone to 'Asia/Kolkata'
    kolkata_tz = pytz.timezone('Asia/Kolkata')

    # Get the current time in UTC using timezone.now()
    my_datetime = timezone.now()

    # Convert the UTC time to the 'Asia/Kolkata' time zone
    my_datetime_in_kolkata = my_datetime.astimezone(kolkata_tz)

    # Convert back to UTC before storing in the database
    return my_datetime_in_kolkata.astimezone(pytz.utc)

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image {self.id} - {self.uploaded_at}"
    

class VisitorPass(models.Model):
    visitor_name = models.CharField(max_length=50)
    date_of_birth = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    purpose = models.CharField(max_length=50)
    date = models.CharField(max_length=10)
    time = models.CharField(max_length=5)
    duration = models.CharField(max_length=5)
    authorized_by = models.CharField(max_length=50)
    qr_img_name = models.CharField(max_length=50)
    pass_id = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(default=get_kolkata_time)
    expire_at = models.DateTimeField(default=get_kolkata_time)
    _encrypted_uuid = models.CharField(max_length=64, unique=True, blank=False, null=False)  # Increased length for SHA-256

    def set_uuid(self, uuid: str):
        # Generate a SHA-256 hash of the UUID
        hash_object = hashlib.sha256(uuid.encode('utf-8'))
        hashed_uuid = base64.b64encode(hash_object.digest()).decode('utf-8')
        self._encrypted_uuid = hashed_uuid

    def get_uuid(self):
        raise NotImplementedError("Direct decryption is not possible with hashing.")

    @property
    def uuid(self):
        raise NotImplementedError("UUID cannot be retrieved after hashing.")

    @uuid.setter
    def uuid(self, value: str):
        self.set_uuid(value)

    class Meta:
        verbose_name_plural = "Visitor Passes"

    def __str__(self):
        return self.pass_id

