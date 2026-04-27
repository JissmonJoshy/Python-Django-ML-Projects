from django.shortcuts import render, redirect
from summary.models import *
from pathlib import Path
from transformers import pipeline
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import nltk
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import face_recognition
import cv2
import os
from VideoSummary import settings
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Create your views here.

def index(request):
    return render(request,"index.html")

def userregistration(request):
    msg = ""
    if request.POST:
        fname = request.POST['fname']
        lname = request.POST['lname']
        age = request.POST['age']
        email = request.POST['email']
        contact = request.POST['contact']
        password = request.POST['password']
        qualif = request.POST['qualif']
        address = request.POST['address']
        purpose = request.POST['purpose']

        email_check = Login.objects.filter(username=email).exists()
        contact_check = User.objects.filter(contact=contact).exists()

        if email_check:
            msg = 'Email Already Registered'
            return render(request, "userregistration.html", {'msg': msg})
        elif contact_check:
            msg = 'Contact Number Already Used'
            return render(request, "userregistration.html", {'msg': msg})
        else:
            try:
                
                login_user = Login.objects.create_user(username=email, email=email, password=password, user_type='User')
                register_user = User.objects.create(
                    firstname=fname,
                    lastname=lname,
                    age=age,
                    contact=contact,
                    qualification=qualif,
                    purpose=purpose,
                    address=address,
                    email=email,
                    loginid=login_user
                )
                register_user.save()
                login_user.save()

                # Capture image
                cap = cv2.VideoCapture(0)
                cv2.waitKey(2000)
                if not cap.isOpened():
                    print("Error: Could not open webcam.")
                    return render(request, "userregistration.html", {'msg': 'Error: Could not open webcam.'})

                ret, frame = cap.read()

                if ret:
                   
                    media_path = os.path.join(settings.MEDIA_ROOT)
                    os.makedirs(media_path, exist_ok=True)  
                    filename = f"{fname+lname}.jpg"
                    filepath = os.path.join(media_path, filename)
                    cv2.imwrite(filepath, frame)  
                    print(f"Image saved at {filepath}")
                    login_user.image = filename
                    login_user.save()

                cap.release()
                cv2.destroyAllWindows()
                
                msg = 'User Registered Successfully'
            except Exception as e:
                print(f"Error: {e}")
                msg = 'Error Occurred While Registering'
                return render(request, "userregistration.html", {'msg': msg})

    return render(request, "userregistration.html", {'msg': msg})

def get_face_encoding(image_path):
    """Extracts face encoding from an image."""
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found!")
        return None
    
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        print(f"No face detected in {image_path}")
        return None 

    return encodings[0]

def login(request):
    msg = ""

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        try:
            email_check = Login.objects.get(username=email)
            password_check = email_check.check_password(password)

            if not email_check.is_active:
                msg = "Account Deleted"
            elif not password_check:
                msg = "Password Entered is Wrong"
            else:
                # Capture user image
                camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not camera.isOpened():
                    return render(request, 'login.html', {'msg': "Error: Could not access the camera."})

                ret, frame = camera.read()
                camera.release()

                if ret:
                    captured_image_path = "captured_image.jpg"
                    cv2.imwrite(captured_image_path, frame)
                    print("Image captured and saved as 'captured_image.jpg'")
                    cv2.imshow("Captured Image", frame)
                    cv2.waitKey(2000)
                    cv2.destroyAllWindows()
                else:
                    return render(request, 'login.html', {'msg': "Error: Could not capture an image."})

                # Store session
                request.session['uid'] = email_check.id

                if email_check.user_type == "User":
                    if email_check.image:  # Ensure image exists in DB
                        registered_image_path = os.path.join("static/media", str(email_check.image))

                        picture_of_me = get_face_encoding(registered_image_path)
                        unknown_picture = get_face_encoding(captured_image_path)

                        if picture_of_me is not None and unknown_picture is not None:
                            results = face_recognition.compare_faces([picture_of_me], unknown_picture, tolerance=0.5)
                            if results[0]:
                                return redirect(f'/userhome?user={email_check.id}')
                            else:
                                msg = "Face recognition failed. Please try again."
                        else:
                            msg = "Comparison not possible due to missing face encodings."
                    else:
                        msg = "No registered image found for this user."
                
                elif email_check.is_superuser:
                    return redirect(f'/adminhome?user={email_check.id}')
                else:
                    msg = "Invalid Usertype"

        except Login.DoesNotExist:
            msg = "Email Not Registered"

    return render(request, 'login.html', {'msg': msg})


def userhome(request):
    uid = request.session['uid']
    user = User.objects.get(loginid__id=uid)
    msg=""
    feedbacks = Feedback.objects.all()
    try:
        user_login = request.GET['user']
        msg="Welcome "+user.firstname
    except:
        pass
    return render(request,"userindex.html",{'msg':msg,'feedbacks':feedbacks,'user':user})

def adminhome(request):
    try:
        msg="Welcome Admin"
    except:
        pass
    return render(request,"adminindex.html",{'msg':msg})


# Summarization
# def get_video_id(url):
#             yt = YouTube(url)
#             return yt.video_id

# def get_subtitles(url, lang="en"):
#     video_id = get_video_id(url)
    
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
#         subtitles = " ".join([f"{item['text']}" for item in transcript])
#         return subtitles
#     except Exception as e:
#         return f"Error: {e}"

# def get_subtitles(url, lang="en"):
#     try:
#         video_id = get_video_id(url)

#         transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
#         transcript = transcript_list.find_transcript([lang])

#         subtitles = " ".join([item['text'] for item in transcript.fetch()])
#         return subtitles

#     except Exception as e:
#         print("Transcript Error:", e)
#         return ""
    
from django.shortcuts import render
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from transformers import pipeline
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from urllib.parse import urlparse, parse_qs
import yt_dlp
import nltk

# Download NLTK data once
nltk.download("punkt")
nltk.download("stopwords")

# Initialize summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def get_video_id(url):
    parsed = urlparse(url)
    hostname = parsed.hostname
    if hostname is None:
        return None
    path = parsed.path
    if "youtu.be" in hostname:
        return path.lstrip("/")
    if "youtube.com" in hostname:
        if path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if path.startswith("/embed/"):
            return path.split("/embed/")[1]
    return None

def get_subtitles(video_url):
    """Get captions if available, otherwise use description."""
    video_id = get_video_id(video_url)
    if not video_id:
        return None, "Invalid YouTube URL"

    # Try captions first
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        text = " ".join([t["text"] for t in transcript]).strip()
        if text:
            return text, None
    except (TranscriptsDisabled, NoTranscriptFound):
        # No captions, fallback
        pass
    except Exception:
        pass

    # Fallback: fetch description
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            description = info.get("description", "").strip()
            if description:
                return description, None
            else:
                return None, "No subtitles or description available"
    except Exception as e:
        return None, f"Failed to fetch video description: {e}"


def videosummary(request):
    summary = ""
    msg = ""

    if request.method == "POST":
        video_url = request.POST.get("video", "").strip()
        if not video_url:
            msg = "Please enter a YouTube link"
            return render(request, "videosummary.html", {"msg": msg, "summary": summary})

        # Get text from captions or description
        text, error = get_subtitles(video_url)
        if error:
            return render(request, "videosummary.html", {"msg": error, "summary": ""})

        # Extractive summarization
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words("english"))
        filtered_words = [w for w in words if w.isalpha() and w not in stop_words]
        word_freq = Counter(filtered_words)
        top_words = [word for word, _ in word_freq.most_common(5)]

        sentences = sent_tokenize(text)
        extractive_summary = " ".join(
            [sent for sent in sentences if any(word in word_tokenize(sent.lower()) for word in top_words)]
        )

        # Abstractive summarization
        input_text = extractive_summary if len(extractive_summary) > 50 else text[:1000]
        try:
            abstractive_summary = summarizer(
                input_text, max_length=150, min_length=40, do_sample=False
            )
            summary = abstractive_summary[0]["summary_text"]
        except Exception:
            summary = extractive_summary

    return render(request, "videosummary.html", {"msg": msg, "summary": summary})
#     try:
#         video_id = get_video_id(url)

#         if not video_id:
#             return ""

#         transcript = YouTubeTranscriptApi.get_transcript(video_id)

#         subtitles = " ".join([item['text'] for item in transcript])

#         return subtitles

#     except Exception as e:
#         print("Transcript Error:", e)
#         return ""

# def get_subtitles(url):
#     try:
#         video_id = get_video_id(url)

#         transcript = YouTubeTranscriptApi.get_transcript(video_id)

#         text = " ".join([t["text"] for t in transcript])

#         return text

#     except Exception as e:
#         print("TRANSCRIPT ERROR:", e)
#         return ""


# def get_subtitles(url):
#     try:
#         video_id = get_video_id(url)

#         transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

#         transcript = transcript_list.find_transcript(['en'])

#         transcript_data = transcript.fetch()

#         text = " ".join([item['text'] for item in transcript_data])

#         return text

#     except Exception as e:
#         print("Transcript Error:", e)
#         return ""




# def videosummary(request):
#     uid = request.session.get('uid')
#     user = User.objects.get(loginid__id=uid)
#     msg = ""
#     summary = ""
#     if request.POST:
#         video=request.POST['video']
#         youtube_url = video
#         text = get_subtitles(youtube_url)
#         print(text)
        
#         nltk.download('punkt')
#         nltk.download('stopwords')
#         words = word_tokenize(text.lower()) 
#         stop_words = set(stopwords.words('english')) 
#         filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
#         word_freq = Counter(filtered_words)
#         top_words = [word for word, _ in word_freq.most_common(5)]  
#         sentences = sent_tokenize(text)  
#         summary_sentences = []
#         for sentence in sentences:
#             words_in_sentence = word_tokenize(sentence.lower())
#             if any(word in words_in_sentence for word in top_words):
#                 summary_sentences.append(sentence)
#         extractive_summary = " ".join(summary_sentences)
#         summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#         input_text = extractive_summary if len(extractive_summary) > 100 else text[:1000]
#         abstractive_summary = summarizer(
#     input_text,
#     max_length=150,
#     min_length=40,
#     do_sample=False
# )
#         print("Extractive Summary:")
#         print(extractive_summary)
#         # summary = extractive_summary
#         print("\nAbstractive Summary:")
#         print(abstractive_summary[0]['summary_text'])
#         abs_sum=abstractive_summary[0]['summary_text']
#         history = Video_History.objects.create(video=video,user=user,summary=abs_sum)
#         history.save()
#         # summary = abs_sum
#         summary = abs_sum

#     return render(request, "videosummary.html", {'msg': msg, 'summary': summary})




def textsummary(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=uid)
    abs_sum=""
    if request.POST:
        text = request.POST['inputtext']
        nltk.download('punkt')
        nltk.download('stopwords')
        words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
        stop_words = set(stopwords.words('english'))  # Define stopwords
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
        word_freq = Counter(filtered_words)
        top_words = [word for word, _ in word_freq.most_common(5)]  # Top 5 important words
        sentences = sent_tokenize(text)  # Tokenize the text into sentences
        summary_sentences = []
        for sentence in sentences:
            words_in_sentence = word_tokenize(sentence.lower())
            if any(word in words_in_sentence for word in top_words):
                summary_sentences.append(sentence)
        extractive_summary = " ".join(summary_sentences)
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        abstractive_summary = summarizer(extractive_summary, max_length=100, min_length=30, do_sample=False)
        print("Extractive Summary:")
        print(extractive_summary)

        print("\nAbstractive Summary:")
        print(abstractive_summary[0]['summary_text'])
        abs_sum=abstractive_summary[0]['summary_text']
        history = Text_History.objects.create(text_input=text,user=user,summary=abs_sum)
        history.save()
    return render(request,"textsummary.html",{'summary':abs_sum})





def user_video_history(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=uid)
    data_video = Video_History.objects.filter(user=user)
    data_text = Text_History.objects.filter(user=user)
    count= data_video.count()
    return render(request,"uservideohistory.html",{'data':data_video,'data2':data_text,'count':count})


def user_profile(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=uid)
    msg=""
    if request.POST:
        try:
            fname=request.POST['fname']
            lname=request.POST['lname']
            age=request.POST['age']
            contact = request.POST['contact']
            qualif = request.POST['qualif']
            address = request.POST['address']
            purpose = request.POST['purpose']
            user.firstname=fname
            user.lastname = lname
            user.age = age
            user.contact = contact
            user.qualification = qualif
            user.address = address
            user.purpose = purpose
            user.save()
            msg="Updated Successfully"
        except:
            msg="Qualification and Purpose Must be selected again make sure you selected it "

    return render(request,"userprofile.html",{'data':user,'msg':msg})

def deleteuserprofile(request):
    uid = request.GET['uid']
    user = Login.objects.get(id=uid)
    user.is_active = 0
    user.save()
    return redirect('/login')

def admin_user(request):
    data = User.objects.all()
    return render(request,"adminusers.html",{'data':data})

def admin_user_details(request):
    uid = request.GET['uid']
    user = User.objects.get(loginid__id=uid)
    return render(request,"adminuserdetails.html",{'data':user})

def admin_user_active(request):
    uid = request.GET['uid']
    user = Login.objects.get(id=uid)
    user.is_active = True
    user.save()
    return redirect(f'/admin_user_details?uid={uid}')

def admin_user_inactive(request):
    uid = request.GET['uid']
    user = Login.objects.get(id=uid)
    user.is_active = False
    user.save()
    return redirect(f'/admin_user_details?uid={uid}')

def user_feedback(request):
    uid = request.session.get('uid')
    user = User.objects.get(loginid__id=uid)
    msg=""
    feeds = Feedback.objects.filter(user=user)
    if request.POST:
        try:
            rating = request.POST['star_rating']
            feed = request.POST['inputtext']
            feedback = Feedback.objects.create(user=user,feedback=feed,rating=rating)
            feedback.save()
            msg="Feedback Added"
        except:
            msg="Click Any Star"
    return render(request,"userfeedback.html",{'msg':msg,'feeds':feeds})


def admin_feedbacks(request):
    data = Feedback.objects.all()
    msg=''
    if request.POST:
            fid= request.POST['fid']
            feed= request.POST['reply']
            feedback = Feedback.objects.get(id=fid)
            feedback.reply = feed
            feedback.save()
            msg="Reply Added Successfully"
    return render(request,"adminfeedbacks.html",{'data':data,'msg':msg})

def user_premium(request):
    data = Premium.objects.all()
    today = datetime.now(timezone.utc)
    print(today,'*********************')
    for d in data:
        datetime_obj = 0
        if ( today > d.offer_till ):
            d.delete()
    return render(request,"userpremium.html",{'data':data})

def admin_premium(request):
    packages = Premium.objects.all()
    count = packages.count()
    msg=''
    if request.POST:
        months = request.POST['months']
        realprice = request.POST['realprice']
        offertill = request.POST['offertill'] 
        offertil = request.POST['offertil']
        offerprice = request.POST['offerprice']
        offertill=offertill+" "+offertil
        
        if count <= 4:
            if realprice > offerprice:
                add_offer= Premium.objects.create(months=months,real_price=realprice,offer_price=offerprice,offer_till=offertill)
                add_offer.save()
                msg="Added Successfully"
            else:
                msg= "Real Price Lesser Than OfferPrice is not acceptable"
        else:
            msg = "Maximum Number Of Packages Can Be Added Is 4"
    return render(request,"adminpremium.html",{'msg':msg,'data':packages})


def admin_premium_delete(request):
    pid = request.GET['pid']
    premium = Premium.objects.get(id=pid)
    premium.delete()
    return redirect('/admin_premium')

def user_payment(request):
    uid = request.session.get('uid')
    user = Login.objects.get(id=uid)
    price = request.GET['price']
    expdate = int(request.GET['expdate'])
    msg=''
    if request.POST:
        try:
            user.premium = 1 
            current_date = datetime.now()
            if expdate > 0:
                future_date = current_date + relativedelta(months=expdate)
                print("Current Date:", current_date.strftime('%Y-%m-%d'))
                print("Future Date:", future_date.strftime('%Y-%m-%d'))
                user.premium_date = future_date.strftime('%d-%m-%Y')
                user.save()
                msg = "Payment Successful"
                return redirect('/user_premium')
            else:
                msg = "Invalid expiration date. Must be greater than 0."

        except Exception as e:
            # Print exception for debugging (optional, avoid in production)
            print(f"Error: {e}")
            msg = "Payment Failed"


    return render(request,"payment.html",{'price':price,'msg':msg})
