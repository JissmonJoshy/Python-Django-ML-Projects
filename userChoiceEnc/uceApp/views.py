from django.shortcuts import render, redirect
from .models import *
import os

from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.
def index(request):
    
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
import random
from django.core.mail import send_mail
from django.conf import settings

def reg(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']

        if User.objects.filter(username=email).exists():
            msg = 'Username already registered..'
            return render(request, 'reg.html', {"msg": msg})

        otp = str(random.randint(100000, 999999))
        request.session['reg_name'] = name
        request.session['reg_email'] = email
        request.session['reg_otp'] = otp

        send_mail(
            subject="Your Registration OTP",
            message=f"Hello {name},\nYour OTP is: {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('otp_verify')
    return render(request, 'reg.html', {"msg": msg})

def otp_verify(request):
    msg = ''
    if request.method == 'POST':
        user_otp = request.POST['otp']
        session_otp = request.session.get('reg_otp')

        if user_otp == session_otp:
            name = request.session.get('reg_name')
            email = request.session.get('reg_email')

            # 🔐 Generate random password
            import secrets, string
            characters = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(characters) for i in range(8))

            user = User.objects.create_user(
                username=email,
                password=password,
                first_name=name,
                is_active=1
            )

            profile = Profile.objects.create(
                user=user,
                viewpassword=password,
                otp=user_otp
            )

            send_mail(
                subject="Your Account Password",
                message=f"Hello {name},\nYour account password is: {password}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            # Clear session
            del request.session['reg_name']
            del request.session['reg_email']
            del request.session['reg_otp']

            msg = "OTP Verified! Password sent to email."
            return render(request, 'otp.html', {"msg": msg, "verified": True})

        else:
            msg = "Invalid OTP, try again."
            return render(request, 'otp.html', {"msg": msg, "verified": False})

    return render(request, 'otp.html', {"msg": msg})

def login(request):
    msg = ''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            usr = User.objects.get(username=email)
            if usr.check_password(password):
                if usr.is_superuser:
                    return redirect('/adminHome')
                else:
                    request.session['uid'] = usr.id
                    return redirect('/userHome')
            else:
                msg = 'Invalid password..'
        else:
            msg = 'User not found..'
    return render(request, 'login.html', {"msg": msg})


def profile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    usr = User.objects.get(id=uid)
    return render(request, 'profile.html', {'user': usr})


# def dlt(request):
#     ids_to_delete = [1, 2, 3, 4, 5]  # multiple IDs
#     ImgToImgDec.objects.filter(id__in=ids_to_delete).delete()
#     return redirect('/')



def adminHome(request):
    return render(request, 'adminHome.html')


def adminViewUsers(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'adminViewUsers.html', {'data': users})

def adminUpdateUserStatus(request):
    uid = request.GET['id']
    user = User.objects.get(id=uid)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('/adminViewUsers')

def adminViewFeedbacks(request):
    blogs = Feedback.objects.filter().order_by("-id")
    return render(request, 'adminViewFeedbacks.html', {'data': blogs})


def userHome(request):
    
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    
    return render(request, 'userHome.html', {'user': user})

def userEnc(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    data =''
    id = ''
    if request.POST:
        image = request.FILES['image']
        dec = DecUpload.objects.create(file=image)
        dec.save()
        return redirect(f"/generate_audio?id={dec.id}")
    return render(request, 'userEnc.html', {"data": data})

def userEncData(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    data =''
    id = ''
    if request.POST:
        audio = request.FILES['audio']
        image = request.FILES['image']
        data = DataStorage.objects.create(user=user, orgImage=image)
        data.save()
        audiofile = os.path.join(BASE_DIR, 'static/media', audio.name)
        default_storage.save(audiofile, ContentFile(audio.read()))
        from .encFile import main
        id = main(data.id, audiofile)
        data = DataStorage.objects.get(id=id)
    return render(request, 'userEnc.html', {"data": data})

def userImageEnc(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    if request.POST:
        image = request.FILES['image']
        key = request.FILES['key']
        dec = ImgToImgDec.objects.create(file=image, key=key)
        dec.save()
        from .imageEnc import decrypt_image_and_show
        decrypt_image_and_show(dec.id)   # ✅ Now works with ImgToImgDec
    return render(request, 'userImageEnc.html')


def userImageEncData(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    data =''
    id = ''
    if request.POST:
        image = request.FILES['image']
        data = ImgToImgEnc.objects.create(user=user, file=image)
        data.save()
        from .imageEnc import encrypt_image_instance
        id = encrypt_image_instance(data.id)
        data = ImgToImgEnc.objects.get(id=id.id)
    return render(request, 'userImageEnc.html', {"data": data})

def userTextEnc(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    data =''
    id = ''
    text = ''
    if request.POST:
        image = request.FILES['image']
        data = EncodedTextDec.objects.create(file=image)
        data.save()
        from .textEnc import decode
        text = decode(data.id)
    return render(request, 'userTextEnc.html', {"text": text})

def userTextEncData(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    data =''
    id = ''
    if request.POST:
        image = request.FILES['image']
        text_area = request.POST['text_area']
        data = EncodedText.objects.create(user=user, inputImage=image)
        data.save()
        from .textEnc import enc_fun
        id = enc_fun(data.id, text_area)
        data = EncodedText.objects.get(id=data.id)
    return render(request, 'userTextEnc.html', {"data": data})


def userFeedback(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    msg = ''
    if request.POST:
        feedback = request.POST['feedback']
        fb = Feedback.objects.create(user=user, feedback=feedback)
        fb.save()
        msg = 'Feedback Submitted..'
    return render(request, 'userFeedback.html', {"msg": msg})




import os
import numpy as np
from PIL import Image
import scipy.io.wavfile as wave
from django.conf import settings
from django.http import FileResponse

def generate_audio(request):
    id = request.GET['id']
    da = DecUpload.objects.get(id=id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(da.file))

    im = Image.open(file_path)
    pixels = im.load()

    left, right = [], []
    width, height = im.size

    # Read encoded audio from red/green channels
    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            left.append(r)
            right.append(g)

    left = np.array(left, dtype=np.float32)
    right = np.array(right, dtype=np.float32)

    # Rescale back to int16
    max_val = 32767
    left = ((left / 255) * 2 * max_val - max_val).astype(np.int16)
    right = ((right / 255) * 2 * max_val - max_val).astype(np.int16)

    stereo_audio = np.column_stack((left, right))

    output_audio_path = os.path.join(settings.MEDIA_ROOT, 'generated_audio.wav')
    wave.write(output_audio_path, 44100, stereo_audio)

    return FileResponse(open(output_audio_path, 'rb'), as_attachment=True, filename='generated_audio.wav')


