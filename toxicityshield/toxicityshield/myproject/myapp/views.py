from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from datetime import date,datetime
from django.db.models import Max
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Avg
from django.template.loader import get_template
from django.db.models import Max
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from django import template
from datetime import datetime

# import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import PIL.Image

# GOOGLE_API_KEY = "AIzaSyCg_onIelbM53UAPf6tosvRt-5fnuOzcPs"
# genai.configure(api_key=GOOGLE_API_KEY)


def to_markdown(text):
    text = text.replace("•", "  *")

def sample(request):
    return render(request,'sample.html')


def index(request):
    return render(request,'index.html')


def profile(request):
    return render(request,'profile.html')

def notification(request):
    return render(request,'notification.html')

def chat(request):
    uid = request.session["uid"]
    
    artist_id = request.GET["id"] 
    artistData = CareTaker.objects.filter(care_id=artist_id)
    print(artist_id) # Get the selected caretaker's ID from the URL
    getChatData = None
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = UserRegister.objects.get(uid=uid)
    
    if artist_id:
        # Filter chat messages based on the selected caretaker's ID
        getChatData = Chat.objects.filter(Q(uid=userid) & Q(cart_id=artist_id))
        artist = UserRegister.objects.get(uid=artist_id)
        obj43=CareTaker.objects.filter(
                care_email=artist.u_email
            ).first()
        name = artist.u_fullname
    else:
        name = ""  # Initialize name if no caretaker is selected
    if request.method == "POST":
        message = request.POST.get("message")
    
        if not obj43:
            print("❌ Caretaker not found for this user")
        elif message:
            Chat.objects.create(
                uid=userid,
                message=message,
                cart_id=obj43,
                time=formatted_time,
                utype="USER"
            )
    return render(request, "User/chat.html", {"artistData": artistData, "getChatData": getChatData, "artistid": name})



def reply(request):
    aid = request.session["care_id"]
    print(aid)
    name=""
    userData = UserRegister.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(Q(cart_id=aid) & Q(uid=id))
    print(getChatData)
    current_time = datetime.now().time()
    formatted_time = current_time.strftime("%H:%M")
    mechanicid = CareTaker.objects.get(care_id=aid)
    if id:
        userid = UserRegister.objects.get(uid=id)
        name=userid.u_fullname
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(uid=userid,message=message,cart_id=mechanicid,time=formatted_time,utype="caretaker")
        sendMsg.save()
    return render(request,"caretaker/chat.html",{"userData": userData, "getChatData": getChatData,"userid":name})


def post_chat(request):
    caretaker_id = request.session.get("care_id")

    post_id = request.GET.get('post_id')
    user_id = request.GET.get('uid')

    post = get_object_or_404(AddPost, post_id=post_id)
    caretaker = get_object_or_404(CareTaker, care_id=caretaker_id)
    user = get_object_or_404(UserRegister, uid=user_id)

    # Get chat messages between caretaker and that user
    getChatData = Chat.objects.filter(
        uid=user,
        cart_id=caretaker
    ).order_by('date','time')

    if request.method == "POST":
        message = request.POST.get("message")

        Chat.objects.create(
            uid=user,
            cart_id=caretaker,
            message=message,
            time=datetime.now().strftime("%H:%M"),
            utype="caretaker"
        )

        return redirect(f"/post_chat/?post_id={post_id}&uid={user_id}")

    context = {
        "post": post,
        "user": user,
        "caretaker": caretaker,
        "getChatData": getChatData
    }

    return render(request, "caretaker/post_chat.html", context)

def add_catetaker(request):
    # uid=request.session.get("uid")
    # obj=UserRegister.objects.filter(uid=uid)
    # context={
    #    'user':obj
    # }

    if request.POST:
        care_fullname=request.POST["care_username"]
        care_email=request.POST["care_email"]
        care_phone=request.POST["care_phone"]
        care_pass=request.POST["care_password"]
        uc_pass=request.POST["care_confirm_password"]
        
        if care_pass==uc_pass:
            if(LoginModule.objects.filter(l_email=care_email).exists()):
                return HttpResponse('<script>alert("CareTaker already exits");window.location.href="/add_catetaker/"</script>')
            else:

                aot=CareTaker.objects.create(care_fullname=care_fullname,
                                        care_email=care_email,
                                        care_phone=care_phone,
                                         care_pass=care_pass,
                                         )
                aot.save()
                aot1=LoginModule.objects.create(l_email=care_email,l_pass=care_pass,l_type="CareTaker",l_status="approved")
                aot1.save()

                return HttpResponse('<script>alert("Succesfully Added");window.location.href="/add_catetaker/"</script>')
        else:    
            return HttpResponse('<script>alert("Password Mismatch ");window.location.href="/add_catetaker/"</script>')
    return render(request,'admin/add_catetaker.html',)


def add_post(request):
    import pytesseract

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    uid = request.session.get("uid")
    obj = UserRegister.objects.filter(uid=uid)
    context = {'user': obj}

    if request.method == "POST":
        current_time = timezone.now()
        uid = request.session.get("uid")
        obj3 = UserRegister.objects.get(uid=uid)

        post_desc = request.POST.get("post_desc")
        post_image = request.FILES.get("post_images")

        # -------------------------------------------------
        # 1️⃣ EMOTION DETECTION MODEL (YOUR OLD ML MODEL)
        # -------------------------------------------------
        import pandas as pd
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression

        mydata = pd.read_csv('mydata1.csv')

        X = mydata['content']
        y = mydata['sentiment']

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        vectorizer = CountVectorizer()
        X_train_vectorized = vectorizer.fit_transform(X_train)
        classifier = LogisticRegression(max_iter=1000)
        classifier.fit(X_train_vectorized, y_train)

        new_samples_vectorized = vectorizer.transform([post_desc])
        predicted_labels = classifier.predict(new_samples_vectorized)[0]

        print("TEXT EMOTION:", predicted_labels)

        # -------------------------------------------------
        # 2️⃣ IMAGE PROCESSING + CHECK AGAINST english.csv
        # -------------------------------------------------
        image_flagged = False
        matched_word = ""

        if post_image:
            import cv2
            import numpy as np
            import re
            from PIL import Image
            import pytesseract

            # -------- Load your english.csv for checking --------
            bad_words_df = pd.read_csv('english.csv')
            bad_words_list = bad_words_df.iloc[:, 0].astype(str).str.lower().tolist()

            # -------- OCR Preprocessing --------
            def preprocess_image_for_ocr(django_file):
                file_bytes = np.asarray(bytearray(django_file.read()), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.fastNlMeansDenoising(gray, h=10)
                thresh = cv2.adaptiveThreshold(
                    gray, 255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )
                return thresh

            def normalize_text(text):
                text = text.lower()
                text = re.sub(r'[^a-z0-9\s]', ' ', text)
                return re.sub(r'\s+', ' ', text).strip()

            # -------- OCR Extract Text --------
            processed_img = preprocess_image_for_ocr(post_image)
            pil_img = Image.fromarray(processed_img)

            raw_text = pytesseract.image_to_string(pil_img)
            normalized_text = normalize_text(raw_text)

            print("OCR TEXT:", normalized_text)

            # -------- Check against english.csv list --------
            for word in bad_words_list:
                if word in normalized_text:
                    image_flagged = True
                    matched_word = word
                    break

            print("⚠ FLAGGED WORD:", matched_word if image_flagged else "None")

        # -------------------------------------------------
        # 3️⃣ HANDLE FLAGGED IMAGE CASE
        # -------------------------------------------------
        if image_flagged:
            return HttpResponse(
                f'<script>alert("POST BLOCKED: Image contains restricted word: {matched_word}");'
                'window.location.href="/add_post/";</script>'
            )

        # -------------------------------------------------
        # 4️⃣ SAVE VALID POST
        # -------------------------------------------------
        aot = AddPost.objects.create(
            post_desc=post_desc,
            post_image=post_image,
            post_status=predicted_labels,  # sentiment result
            uid=obj3,
            u5=current_time
        )
        aot.save()

        return HttpResponse(
            '<script>alert("Successfully Posted"); window.location.href="/add_post/";</script>'
        )

    return render(request, 'user/add_post.html', context)


def add_comment(request):
    if request.method == "POST":
        uid = request.session.get("uid")
        post_id = request.POST.get("post_id")
        comment_text = request.POST.get("comment_text")
        
        if not uid:
            return redirect('/login')

        user_obj = UserRegister.objects.get(uid=uid)
        post_obj = AddPost.objects.get(post_id=post_id)
        
        import pandas as pd
        import re

        # -------- Load bad words list --------
        bad_words_df = pd.read_csv('english.csv')
        bad_words_list = bad_words_df.iloc[:, 0].astype(str).str.lower().tolist()

        def normalize_text(text):
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', ' ', text)
            return re.sub(r'\s+', ' ', text).strip()

        normalized_comment = normalize_text(comment_text)
        
        comment_flagged = False
        matched_word = ""

        # Check for bad words in the comment text
        for word in bad_words_list:
            # Check if the word exists as a standalone word or within the text
            # This follows the logic in add_post: "if word in normalized_text"
            if word in normalized_comment:
                comment_flagged = True
                matched_word = word
                break
        
        if comment_flagged:
            return HttpResponse(
                f'<script>alert("COMMENT BLOCKED: Comment contains restricted word: {matched_word}");'
                'window.location.href="/user_home/";</script>'
            )
        
        # -------------------------------------------------
        # EMOTION DETECTION (Optional, but matches post logic)
        # -------------------------------------------------
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression

        mydata = pd.read_csv('mydata1.csv')
        X = mydata['content']
        y = mydata['sentiment']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        vectorizer = CountVectorizer()
        X_train_vectorized = vectorizer.fit_transform(X_train)
        classifier = LogisticRegression(max_iter=1000)
        classifier.fit(X_train_vectorized, y_train)

        new_samples_vectorized = vectorizer.transform([comment_text])
        predicted_sentiment = classifier.predict(new_samples_vectorized)[0]

        # Save comment
        Comment.objects.create(
            post_id=post_obj,
            uid=user_obj,
            comment_text=comment_text,
            comment_status=predicted_sentiment
        )
        return HttpResponse('<script>alert("Commented successfully");window.location.href="/user_home/"</script>')
    return redirect('/user_home/')






register = template.Library()

@register.filter

def post_time_ago(post_time):
    # Convert post_time to datetime object if it's a string
    if isinstance(post_time, str):
        post_time = datetime.strptime(post_time, '%Y-%m-%d %H:%M:%S')

    # Calculate the time difference in seconds
    time_diff = timezone.now() - timezone.localtime(post_time)

    # Convert time difference to minutes
    minutes = time_diff.total_seconds() / 60

    # Determine the appropriate time unit based on the time difference
    if minutes < 60:
        return f'{int(minutes)} min ago'
    elif minutes < 1440:
        return f'{int(minutes / 60)} hr ago'
    else:
        return 'More than a day ago'


def view_post(request):
    uid = request.session.get("uid")
    obj = AddPost.objects.filter(uid=uid).order_by('-post_id')
    for post in obj:
        post.comments = Comment.objects.filter(post_id=post).order_by('-comment_id')
    context={
        'post':obj

    }

    return render(request, 'user/view_post.html',context)




def caretaker_home(request):
    uid = request.session.get("uid")
    obj = AddPost.objects.all().order_by('-post_id')
    for post in obj:
        # Safe date parsing
        if post.u5 and '-' in post.u5 and ':' in post.u5:
            try:
                post_time_without_timezone = post.u5.split('+')[0].split('.')[0]
                post.post_date = datetime.strptime(post_time_without_timezone, '%Y-%m-%d %H:%M:%S')
            except:
                post.post_date = None
        else:
            post.post_date = None
            
        post.comments = Comment.objects.filter(post_id=post).order_by('-comment_id')
    context={
        'post':obj
    }

    return render(request, 'caretaker/caretaker_home.html',context)




def pay(request):
    id = request.GET.get("id")
    uid=request.session.get("uid")


   

    return render(request,'user/pay.html',{'id': id})


def chatbot(request):
    
    answer = ""
    question = ""
    if request.POST:
        question = request.POST["question"]
        # GENERATION

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(question)
        print(response.text)
        to_markdown(response.text)

        # img = PIL.Image.open("maths-gemini.webp")

        # model = genai.GenerativeModel("gemini-pro-vision")

        # response = model.generate_content(
        #     [
        #         "Solve the equation in the image",
        #         img,
        #     ],
        #     stream=True,
        # )
        # response.resolve()

        to_markdown(response.text)
        print(response.text)
        answer = response.text

    # return render(
    #     request, "student/ask_question.html", {"question": question, "answer": answer}
    # )


    return render(request, 'user/chatbot.html',{"question": question, "answer": answer})


def view_catetaker(request):
    # uid = request.session.get("uid")
    obj = CareTaker.objects.all()
    context={
        'care':obj

    }


  

    return render(request, 'admin/view_catetaker.html',context)

def chat_caretaker(request):
    uid = request.session.get("uid")
    caretakers = CareTaker.objects.all()
    
    # Get all paid payments for this user
    paid_payments = Payment.objects.filter(uid=uid, b_status="Paid")

    # Create a set of paid caretaker IDs
    paid_caretakers = {payment.care_id_id for payment in paid_payments}

    context = {
        'care': caretakers,
        'paid_caretakers': paid_caretakers,  # Pass the set of paid caretaker IDs
    }

    return render(request, 'user/chat_caretaker.html', context)



def view_feed_back(request):
    # uid = request.session.get("uid")
    obj = FeedBack.objects.all()
    context={
        'care':obj

    }


  

    return render(request, 'caretaker/view_feed_back.html',context)\
    

def view_payment_paisa(request):
    id = request.session.get("care_id")
    print(id)
    obj = Payment.objects.filter(care_id=id)
    context={
        'care':obj

    }

    print(obj)
  

    return render(request, 'caretaker/view_payment_paisa.html',context)





from django.db.models import Count, Q

def view_user(request):
    # Fetch all users and annotate with sad post count
    obj = UserRegister.objects.annotate(
        sad_posts_count=Count('addpost', filter=Q(addpost__post_status='sadness'))
    )
    
    context = {
        'care': obj
    }

    return render(request, 'admin/view_user.html', context)
from django.shortcuts import get_object_or_404, redirect
def send_counseling_message(request):
    id = request.GET['id']
    print(id)
    user = get_object_or_404(UserRegister, uid=id)
        
        # Create a counseling message entry in the database
    CounselingMessage.objects.create(
            uid=user,
            message="You need counseling as soon as possible"
        )
    return redirect('/view_user')

def feedback(request):
    if request.POST:
        uid=request.session.get("uid")
        obj1=UserRegister.objects.get(uid=uid)
        feed_name=request.POST["feed_name"]
        feed_email=request.POST["feed_email"]
        saysomething=request.POST["feed_message"]
        aot=FeedBack.objects.create(feed_name=feed_name,feed_email=feed_email,saysomething=saysomething,uid=obj1)
        aot.save()

        return HttpResponse('<script>alert("Thank you for feedback");window.location.href="/feed_back"</script>') 
    return render(request,'user/feedback.html')


def user_home(request):
    uid = request.session.get("uid")
    obj = UserRegister.objects.filter(uid=uid)
    obj3 = AddPost.objects.all().order_by('-post_id')
    obj4=AddPost.objects.filter(uid=uid)
    obj5=CounselingMessage.objects.filter(uid=uid)

    # Convert post_time strings to datetime objects
    for post in obj3:
        # Safe date parsing
        if post.u5 and '-' in post.u5 and ':' in post.u5:
            try:
                post_time_without_timezone = post.u5.split('+')[0].split('.')[0]
                post.post_date = datetime.strptime(post_time_without_timezone, '%Y-%m-%d %H:%M:%S')
            except:
                post.post_date = None
        else:
            post.post_date = None
            
        # Fetch comments for each post
        post.comments = Comment.objects.filter(post_id=post).order_by('-comment_id')

    context = {
       'user': obj,
       'post': obj3,
       'image':obj4,
       'msg':obj5
    }

    return render(request, 'user/user_home.html', context)


def admin_home(request):
    obj3 = AddPost.objects.all().order_by('-post_id')

    for post in obj3:
        # Safe date parsing
        if post.u5 and '-' in post.u5 and ':' in post.u5:
            try:
                post_time_without_timezone = post.u5.split('+')[0].split('.')[0]
                post.post_date = datetime.strptime(post_time_without_timezone, '%Y-%m-%d %H:%M:%S')
            except:
                post.post_date = None
        else:
            post.post_date = None
            
        # Fetch comments
        post.comments = Comment.objects.filter(post_id=post).order_by('-comment_id')

    context = {
       'post': obj3,
    }

    return render(request, 'admin/admin_home.html', context)



def payment(request,id):
    # id=request.GET.get("id")
    obj7=CareTaker.objects.get(care_id=id)
    print(id)
    uid = request.session.get("uid")
    obj4=UserRegister.objects.get(uid=uid)

    email=CareTaker.objects.filter(care_id=id)
    aot=Payment.objects.create(uid=obj4,care_id=obj7,b_status="Paid")
    aot.save()
    # opp=CareTaker.objects.filter(care_id=id,).update(u8="Paid")

    return HttpResponse('<script>alert("Payment Success");window.location.href="/chat_caretaker/"</script>')


def delete_post(request):
    id=request.GET["id"]
    print(id)
    email=AddPost.objects.filter(post_id=id)
    opp=AddPost.objects.filter(post_id=id).delete()
    return HttpResponse('<script>alert("Deleted");window.location.href="/view_post/"</script>')



def care_delete(request):
    id=request.GET["id"]
    print(id)
    email=CareTaker.objects.filter(care_id=id)
    opp=CareTaker.objects.filter(care_id=id).delete()

    return HttpResponse('<script>alert("Deleted");window.location.href="/view_catetaker/"</script>')
    



def update_profile(request):
    uid=request.session.get("uid")
    print(uid)
    obj=UserRegister.objects.filter(uid=uid)
    context={
       'user':obj
    }
     
    if request.POST:
        a_name=request.POST["username"]
        a_email=request.POST["email"]
        a_phone=request.POST["phone"]
        u_profile=request.POST["u_profile"]
        u_from=request.POST["u_from"]
        u_about=request.POST["u_about"]
        u1=request.POST["u1"]
        u2=request.POST["u2"]
        profile_image=request.FILES.get("Profile_image")
        back_image=request.FILES.get("background_image")

        data=UserRegister.objects.get(uid=uid)
        if profile_image:
            data.profile_image=profile_image
            data.save()
        if back_image:
            data.post_image=back_image
            data.save()

        
        aot=UserRegister.objects.filter(uid=uid).update(u_fullname=a_name,
                                   u_email=a_email,
                                   u_phone=a_phone,
                                   u_profile=u_profile,
                                   u_from=u_from,
                                   u_about=u_about,
                                   u1=u1,
                                   u2=u2,

                                 
                                   )
        # aot.save()
        return HttpResponse('<script>alert("Updated succesfully");window.location.href="/update_profile/"</script>')
    return render(request,'user/update_profile.html',context)



def login(request):

      if request.POST:
        log_user=request.POST["log_email"]
        log_pass=request.POST["log_password"]
        request.session["lol"]=log_user
        aot=LoginModule.objects.filter(Q(l_email=log_user)&Q(l_pass=log_pass))
        if aot:
            if(aot[0].l_type=="user"):
                if(aot[0].l_status=="approved"):
                    aot1=UserRegister.objects.filter(u_email=log_user)
                    request.session["uid"]=aot1[0].uid
                    return HttpResponse('<script>alert("Logged in as user");window.location.href="/user_home"</script>')
        
            elif(aot[0].l_type=="CareTaker"):
                if(aot[0].l_status=="approved"):
                    aot1=CareTaker.objects.filter(care_email=log_user)
                    request.session["care_id"]=aot1[0].care_id
                    return HttpResponse('<script>alert("Loggedin as CareTaker");window.location.href="/caretaker_home"</script>')
                else:
                   return HttpResponse('<script>alert("Please Wait For Approval");window.location.href="/login"</script>')
           
            # elif(aot[0].l_type=="SalesStaff"):
            #     if(aot[0].l_status=="approved"):
            #         aot1=AddSalesStaff.objects.filter(staff_email=log_user)
            #         request.session["staff_id"]=aot1[0].staff_id
            #         return HttpResponse('<script>alert("Loggedin as SalesStaff");window.location.href="/sales_staff_home"</script>')
            #     else:
            #        return HttpResponse('<script>alert("Please Wait For Approval");window.location.href="/login"</script>')
           
            elif(aot[0].l_type=="admin"):  
                    aot=LoginModule.objects.filter(Q(l_email=log_user)&Q(l_pass=log_pass))  
                    return HttpResponse('<script>alert("Logged in as admin");window.location.href="/admin_home"</script>')                          
        else:
                return HttpResponse('<script>alert("Invalid Username and Password");window.location.href="/login"</script>')
        



      return render(request,'login.html')

def register_user(request):
     if request.POST:
        fullname=request.POST["user_name"]
        email=request.POST["user_email"]
        phone=request.POST["user_phone"]
        # address=request.POST["user_address"]
        u_pass=request.POST["user_password"]
        uc_pass=request.POST["user_confirm_password"]
        
        if u_pass==uc_pass:
            if(LoginModule.objects.filter(l_email=email).exists()):
                return HttpResponse('<script>alert("Email already exits");window.location.href="/register"</script>')
            else:
                aot=UserRegister.objects.create(u_fullname=fullname,u_email=email,u_phone=phone,u_pass=u_pass,u1="approved")
                aot.save()
                aot1=LoginModule.objects.create(l_email=email,l_pass=u_pass,l_type="user",l_status="approved")
                aot1.save()
                return HttpResponse('<script>alert("Registered as user");window.location.href="/login"</script>')
        else:
            return HttpResponse('<script>alert("Password Mismatch ");window.location.href="/register_user"</script>')


     return render(request,'register_user.html')





