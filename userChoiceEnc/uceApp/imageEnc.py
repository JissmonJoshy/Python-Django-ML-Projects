import os
import math
import io
import numpy as np
from PIL import Image
from cryptography.fernet import Fernet

from django.core.files.base import ContentFile
from django.conf import settings
from uceApp.models import ImgToImgEnc  # Replace `yourapp` with your app name


def encrypt_image_instance(instance_id):
    try:
        instance = ImgToImgEnc.objects.get(id=instance_id)
    except ImgToImgEnc.DoesNotExist:
        raise ValueError(f"No ImgToImgEnc entry with ID {instance_id}")

    if not instance.file:
        raise ValueError(f"No input file associated with ID {instance_id}")

    # Load image
    with Image.open(instance.file.path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

    # Generate and encrypt
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted_bytes = cipher.encrypt(img_bytes)

    # Convert to image
    data_len = len(encrypted_bytes)
    side = math.ceil(math.sqrt(data_len))
    padded_len = side * side
    padded_data = encrypted_bytes + b'\0' * (padded_len - data_len)
    array = np.frombuffer(padded_data, dtype=np.uint8).reshape((side, side))
    img_data = Image.fromarray(array, mode='L')

    # Save encrypted image to memory
    encrypted_img_io = io.BytesIO()
    img_data.save(encrypted_img_io, format='PNG')
    encrypted_img_io.seek(0)

    # Save key to memory
    key_io = io.BytesIO()
    key_io.write(key)
    key_io.seek(0)

    # Update model
    instance.output.save(f'encrypted_{instance_id}.png', ContentFile(encrypted_img_io.read()))
    instance.key.save(f'key_{instance_id}.key', ContentFile(key_io.read()))
    instance.save()

    return instance



def decrypt_image_and_show(instance_id):
    from uceApp.models import ImgToImgDec
    try:
        instance = ImgToImgDec.objects.get(id=instance_id)
    except ImgToImgDec.DoesNotExist:
        raise ValueError(f"No ImgToImgDec entry with ID {instance_id}")

    if not instance.file or not instance.key:
        raise ValueError("Missing encrypted image or key.")

    # Read key
    key = instance.key.read()
    cipher = Fernet(key)

    # Load encrypted image and convert to bytes
    encrypted_img = Image.open(instance.file.path).convert("L")
    encrypted_array = np.array(encrypted_img)
    encrypted_bytes = encrypted_array.tobytes()

    # Try decryption (handle padding errors)
    try:
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
    except Exception:
        decrypted_bytes = cipher.decrypt(encrypted_bytes.rstrip(b'\0'))

    # Convert decrypted bytes to image and show
    img = Image.open(io.BytesIO(decrypted_bytes))
    img.show()
