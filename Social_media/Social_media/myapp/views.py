from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate
from datetime import datetime
from django.db.models import Q
import imghdr
from django.http import HttpResponseBadRequest
import numpy as np
import pandas as pd
np.random.seed(42)
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout

# Create your views here.


def index(request):
    return render(request, "home.html")

from django.contrib.auth import authenticate, login

def log(request):
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user) 
            if user.type == "Admin":
                # request.session["lid"] = user.id
                return redirect("/admin_home")
            elif user.type == "User":
                uid = user.id
                request.session["uid"] = uid
                return redirect("/user_home")
            else:
                messages.error(
                    request, "<script>alert('User Type not Defined')</script>"
                )
                return redirect("/")
        else:
            messages.error(
                request, "<script>alert('Icorrect Email of Password')<\/script>"
            )

    return render(request, "signin.html")


def reg(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        image = request.FILES["image"]
        password = request.POST["password"]

        if Login.objects.filter(email=email).exists():
            messages.error(request, "Email or password already taken")
        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                type="User",
                viewpass=password,
                is_active=1,
            )
            logUser.save()

            userReg = Userreg.objects.create(
                name=name,
                email=email,
                phone=phone,
                image=image,
                loginid=logUser,
            )
            userReg.save()
            return HttpResponse(f"<script>alert('Successfully Registered'); window.location= '/'</script>")
            
    return render(request, "signup.html")


def udp(request):
    de = Login.objects.filter(id=8).update(type="Admin")
   
    return redirect("/user_home")


def user_home(request):
    # getUid
    uid = request.session["uid"]
    print(uid)
    Uid = Userreg.objects.get(loginid=uid)
    # show users
    view = Userreg.objects.exclude(loginid=uid)
    # profile Details
    profile = Userreg.objects.get(loginid=uid)
    #follower Profile
    follow=Follow.objects.filter(following=Uid)    
    print("followings :",follow)
    
    #view Stories
    stories=Stories.objects.all()
    # print("stories : ",stories)

    # check to click the person is liked

    likeData = Like.objects.filter(liker=Uid)
    posts_liked_by_user = likeData.values_list("pid_id", flat=True)
    posts_only_liked_by_user = Posts.objects.filter(id__in=posts_liked_by_user)
    ids_of_posts_only_liked_by_user = posts_only_liked_by_user.values_list(
        "id", flat=True
    )

    # to view all Posts

    Post = Posts.objects.filter(status="good")

    # View All Comments

    view_comment = Comments_on_Posts.objects.all()

    # Add Posts
    
    # if "pos" in request.POST:
    #     caption = request.POST["caption"]
    #     image = request.FILES["file"]
    #     # =================================================================
    #     dataset_path = 'Dataset 1.csv'
    #     df = pd.read_csv(dataset_path)

    #     # Separate features and labels
    #     X = df['Text'].astype(str)
    #     y = df['Suicide']

    #     # Tokenize and pad sequences
    #     max_words = 10000
    #     max_len = 500
    #     tokenizer = Tokenizer(num_words=max_words)
    #     tokenizer.fit_on_texts(X)
    #     X_seq = tokenizer.texts_to_sequences(X)
    #     X_pad = pad_sequences(X_seq, maxlen=max_len)

    #     # Split the data into training and testing sets
    #     X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.2, random_state=42)

    #     # Build the CNN model
    #     model = Sequential()
    #     model.add(Embedding(max_words, 50, input_length=max_len))
    #     model.add(Conv1D(128, 5, activation='relu'))
    #     model.add(GlobalMaxPooling1D())
    #     model.add(Dense(64, activation='relu'))
    #     model.add(Dropout(0.5))
    #     model.add(Dense(1, activation='sigmoid'))

    #     # Compile the model
    #     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    #     # Train the model
    #     model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

    #     # Evaluate the model
    #     loss, accuracy = model.evaluate(X_test, y_test)
    #     print(f'Test Accuracy: {accuracy}')

    #     # Make predictions
    #     # Replace 'your_text' with the actual text you want to classify
    #     # new_texts = ["@dizzyhrvy that crap took me forever to put together. iÃ¢Â€Â™m going to go sleep for DAYS"]
    #     new_texts=[caption]
    #     new_texts_seq = tokenizer.texts_to_sequences(new_texts)
    #     new_texts_pad = pad_sequences(new_texts_seq, maxlen=max_len)
    #     predictions = model.predict(new_texts_pad)

    #     # Convert predictions to labels
    #     predicted_labels = ["suicidal" if pred > 0.5 else "non-suicidal" for pred in predictions]
    #     print(f'Predicted Labels+++++++++++++++++++++++++++++++++: {predicted_labels}')
    #     if predicted_labels[0]=="suicidal":
    #         ins = Posts.objects.create(
    #         uid=Uid, image=image, caption=caption, likes=0, comments=0,status="bad"
    #         )
    #         ins.save()
    #         return HttpResponse("<script>alert('cannot post this');window.location.href='/user_home'</script>")
    #         # return redirect("/user_home")
    #     else:
    #     # =================================================================
    #         ins = Posts.objects.create(
    #         uid=Uid, image=image, caption=caption, likes=0, comments=0
    #         )
    #         ins.save()
    #         messages.success(request, "<script>alert('image Post saved')</script>")
    #         return redirect("/user_home")
    if "pos" in request.POST:
        caption = request.POST["caption"]
        image = request.FILES["file"]

        dataset_path = "Dataset 1.csv"
        df = pd.read_csv(dataset_path)

        # Separate features and labels
        X = df["Text"].astype(str)
        y = df["Suicide"]

        # Tokenize
        max_words = 10000
        max_len = 500

        tokenizer = Tokenizer(num_words=max_words)
        tokenizer.fit_on_texts(X)

        X_seq = tokenizer.texts_to_sequences(X)
        X_pad = pad_sequences(X_seq, maxlen=max_len)

        # Train Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X_pad, y, test_size=0.2, random_state=42
        )

        # CNN Model
        model = Sequential()
        model.add(Embedding(max_words, 50, input_length=max_len))
        model.add(Conv1D(128, 5, activation="relu"))
        model.add(GlobalMaxPooling1D())
        model.add(Dense(64, activation="relu"))
        model.add(Dropout(0.5))
        model.add(Dense(1, activation="sigmoid"))

        model.compile(
            optimizer="adam",
            loss="binary_crossentropy",
            metrics=["accuracy"]
        )

        # Train Model
        model.fit(X_train, y_train, epochs=5, batch_size=32)

        # Test Caption
        new_text = [caption]

        new_seq = tokenizer.texts_to_sequences(new_text)
        new_pad = pad_sequences(new_seq, maxlen=max_len)

        prediction = model.predict(new_pad)[0][0]

        print("Caption:", caption)
        print("Prediction Score:", prediction)

        # Suicide Detection
        if prediction > 0.5:

            Posts.objects.create(
                uid=Uid,
                image=image,
                caption=caption,
                likes=0,
                comments=0,
                status="bad"
            )

            return HttpResponse(
                "<script>alert('Suicidal content detected! Post blocked');window.location='/user_home'</script>"
            )

        else:

            Posts.objects.create(
                uid=Uid,
                image=image,
                caption=caption,
                likes=0,
                comments=0,
                status="good"
            )

            messages.success(request, "Post uploaded successfully")

            return redirect("/user_home")

    # Add Post with Step by steps
    
    
    
    if "Post" in request.POST:
        caption = request.POST["caption"]
        location = request.POST["location"]
        file = request.FILES["posts"]
        
        if file:
            image_type = imghdr.what(file)
            if image_type in ["jpeg", "png", "gif","jpg"]:  
                ins = Stories.objects.create(
                    uid=Uid,
                    file=file,
                    caption=caption,
                    type="Image"
                )
                ins.save()
                print("Image Successfully added")
                return redirect("/user_home")
                
            else:
                ins = Stories.objects.create(
                    uid=Uid,
                    file=file,
                    caption=caption,
                    type="Video"
                )
                ins.save()
                print("Image Successfully added")
                return redirect("/user_home")
        
        messages.success(request, "Image Post saved")
        return redirect("/user_home")

    
    # add comments

    if "comments" in request.POST:
        cmt = request.POST["cmt"]
        pid = request.POST["pid"]
        Pid = Posts.objects.get(id=pid)

        add = Comments_on_Posts.objects.create(uid=Uid, comment=cmt, pid=Pid)
        add.save()

        update_post = Posts.objects.get(id=pid)
        update_post.comments += 1
        update_post.save()
        


    context = {
        "view": view,
        "profile": profile,
        "Posts": Post,
        "stories": stories,
        "view_comment": view_comment,
        "follow": follow,
        "likeData": ids_of_posts_only_liked_by_user,
    }

    return render(request, "User/home.html", context)


# def admin_home(request):
#     view = Userreg.objects.all()
#     stories=Stories.objects.all()
#     Post = Posts.objects.filter(status="good")
#     view_comment = Comments_on_Posts.objects.all()
#     context = {
#         "view": view,
#         "Posts": Post,
#         "stories": stories,
#         "view_comment": view_comment,
#         "follow": follow,

#     }

#     return render(request, "Admin/home.html", context)


# def admin_home(request):
#     view = Userreg.objects.all()
#     stories = Stories.objects.all()

#     good_posts = Posts.objects.filter(status="good")
#     bad_posts = Posts.objects.filter(status="bad")

#     view_comment = Comments_on_Posts.objects.all()

#     context = {
#         "view": view,
#         "good_posts": good_posts,
#         "bad_posts": bad_posts,
#         "stories": stories,
#         "view_comment": view_comment,
#     }

#     return render(request, "Admin/home.html", context)


def admin_home(request):

    view = Userreg.objects.all()
    stories = Stories.objects.all()
    posts = Posts.objects.all()
    view_comment = Comments_on_Posts.objects.all()

    context = {
        "view": view,
        "posts": posts,
        "stories": stories,
        "view_comment": view_comment,
    }

    return render(request,"Admin/home.html",context)


# def user_profile(request):
#     uid = request.session["uid"]
#     view = Userreg.objects.filter(loginid=uid)
#     # show users
#     profile = Userreg.objects.exclude(loginid=uid)
#     print("efewfdwefewf", profile)

#     # view Posts
#     posts = Posts.objects.filter(uid__loginid=uid)
#     print("posts : ", posts,uid)

#     return render(
#         request,
#         "User/profile.html",
#         {"view": view, "profiles": profile, "posts": posts},
#     )


# def user_profile(request):
#     userid = request.GET.get("uid")

#     if not userid:
#         return HttpResponse("User ID missing")

#     user_obj = Userreg.objects.get(loginid=userid)
#     posts = Posts.objects.filter(uid=user_obj)

#     return render(request, "Admin/view_user_profile.html", {
#         "userprofile": user_obj,
#         "posts": posts
#     })
# from django.shortcuts import render, get_object_or_404
# from .models import Userreg, Posts

def user_profile(request):
    userid = request.GET.get("uid")

    if not userid:
        return HttpResponse("User ID missing")

    user_obj = get_object_or_404(Userreg, loginid=userid)
    posts = Posts.objects.filter(uid=user_obj)

    return render(request, "Admin/view_user_profile.html", {
        "userprofile": user_obj,
        "posts": posts
    })


from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse

def admin_send_message(request):

    # ✅ CHECK ADMIN LOGIN
    admin_id = request.session.get("lid")
    if not admin_id:
        return redirect("/")   # not logged in

    # ✅ GET ADMIN
    admin = Login.objects.get(id=admin_id)

    # ✅ CHECK TYPE (THIS IS WHAT YOU WANT)
    if admin.type != "Admin":
        return HttpResponse("You are not admin")

    # ✅ GET USER
    uid = request.GET.get("uid")
    receiver = Userreg.objects.filter(id=uid).first()

    if not receiver:
        return HttpResponse("User not found")

    # ✅ SEND MESSAGE
    if request.method == "POST":
        msg = request.POST.get("msg")
        file = request.FILES.get("fileInput")

        if msg or file:
            AdminChat.objects.create(
                sender_admin=admin,
                receiver_user=receiver,
                message=msg,
                file=file,
                content_type="text" if msg else "file",
                date=datetime.now().date(),
                time=datetime.now().strftime("%H:%M"),
            )

        return redirect(f"/admin_send_message/?uid={uid}")

    # ✅ LOAD CHAT
    chatData = AdminChat.objects.filter(
        sender_admin=admin,
        receiver_user=receiver
    ).order_by("timestamp")

    return render(request, "Admin/admin_send_message.html", {
        "chatData": chatData,
        "pro": receiver
    })


def user_chat(request):
    uid = request.session.get("uid")

    if not uid:
        return redirect("/login/")

    user = Userreg.objects.get(loginid=uid)

    chats = AdminChat.objects.filter(
        receiver_user=user
    ) | AdminChat.objects.filter(
        sender_user=user
    )

    chats = chats.order_by("timestamp")

    return render(request, "User/chat.html", {"chats": chats})

from datetime import datetime

def send_reply(request):
    if request.method == "POST":

        uid = request.session.get("uid")
        if not uid:
            return redirect("/login/")

        user = Userreg.objects.get(loginid=uid)
        admin = Login.objects.filter(type="admin").first()

        message = request.POST.get("msg")   # MUST match HTML

        now = datetime.now()

        AdminChat.objects.create(
            sender_user=user,
            receiver_admin=admin,
            message=message,
            content_type="text",
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M")
        )

        return redirect("/user_chat/")
    

def update_user_profile(request):
    uid = request.session["uid"]
    view = Userreg.objects.filter(loginid=uid)
    Uid = Userreg.objects.get(loginid=uid)

    if "profile" in request.POST:
        username = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        bio = request.POST["bio"]
        print("Data", username, email, phone, bio)

        image = request.FILES["image"]
        up_img = Userreg.objects.get(loginid__id=uid)
        up_img.image = image
        up_img.save()

        update = Userreg.objects.filter(loginid=uid).update(
            username=username, email=email, phone=phone, bio=bio
        )

    elif "password" in request.POST:
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match")
            return redirect("/update_user_profile")
        else:
            up = Userreg.objects.get(loginid=Uid)
            up.set_password(new_password)
            up.save()

    return render(request, "User/setting.html", {"view": view})


def like(request):
    uid = request.session["uid"]
    Uid = Userreg.objects.get(loginid=uid)
    pid = request.GET.get("pid")
    Pid = Posts.objects.get(id=pid)

    if not Like.objects.filter(liker=Uid, pid=pid).exists():
        add_like = Like.objects.create(liker=Uid, pid=Pid)
        add_like.save()
        update_like = Posts.objects.get(id=pid)
        update_like.likes += 1
        update_like.save()
    else:
        add_like = Like.objects.filter(liker=Uid, pid=Pid).delete()
        update_like = Posts.objects.get(id=pid)
        update_like.likes -= 1
        update_like.save()

    return redirect("/user_home")


def follow(request):
    other_userid = request.GET.get("userid")
    uid = request.session["uid"]
    Uid = Userreg.objects.get(loginid=uid)
    other_user = Userreg.objects.get(loginid=other_userid)

    if not Follow.objects.filter(
        following__loginid=other_userid, follower__loginid=uid).exists():
        add_follow = Follow.objects.create(follower=Uid, following=other_user)
        add_follow.save()
        update_follow = Userreg.objects.get(loginid=uid)
        update_follow.following += 1
        update_follow.save()
        update_following = Userreg.objects.get(loginid=other_userid)
        update_following.followers += 1
        update_following.save()
        

    else:
        add_follow = Follow.objects.filter(
            follower__loginid=uid, following__loginid=other_userid
        ).delete()
        update_follow = Userreg.objects.get(loginid=other_userid)
        update_follow.followers -= 1
        update_follow.save()

        update_following = Userreg.objects.get(loginid=uid)
        update_following.following -= 1
        update_following.save()

    return redirect(f"/users_profile?uid={other_userid}")


def users_profile(request):
    #get other userid
    userid = request.GET.get("uid")
    Uid = Userreg.objects.get(loginid=userid)
    view = Userreg.objects.filter(loginid=userid)
    
    #view Post
    view_post = Posts.objects.filter(uid=Uid)

    uid = request.session["uid"]
    curent_user = Userreg.objects.get(loginid=uid)
    
    #check friendlits list
    friend=Friends_list.objects.filter(user=curent_user,friend=Uid)
    
    #check follow list
    check_follow=Follow.objects.filter(following=Uid,follower=curent_user)
    print("following : ",check_follow)
    
    # show users
    profile = Userreg.objects.exclude(loginid=uid)

    return render(
        request,
        "User/users_profile.html",
        {"userprofile": view, "posts": view_post, "profiles": profile,"friend_list":friend,"check_follow":check_follow})


def common(request):
    uid = request.session["uid"]
    Uid = Userreg.objects.get(loginid=uid)
    # show users
    view = Userreg.objects.exclude(loginid=uid)
    # profile Details
    return render(request, "User/common.html", {"profile": view})


from datetime import datetime


def messageses(request):
    print(request.user,"HELLO")
    # userid for Chat
    usersid = request.GET.get("uid")
    receiver = Userreg.objects.get(loginid=usersid)
    print(receiver)
    # show users
    time = datetime.now().time()
    date = datetime.now().date()
    

    formatted_time = time.strftime("%I:%M %p")
    formatted_date = date.strftime("%B %d")
    
    print(formatted_time,formatted_date)

    uid = request.session["uid"]
    profile = Userreg.objects.exclude(loginid=uid)
    sender = Userreg.objects.get(loginid=uid)

    print(uid, "SENDER")
    print(usersid, "RECEIVER")

    ############CHAT DATA################
    chatData = Chat.objects.filter(
        Q(sender__loginid=uid) & Q(receiver__loginid=usersid)
        | Q(sender__loginid=usersid) & Q(receiver__loginid=uid)
    ).order_by("timestamp")
    
    last_message = Chat.objects.filter(
    Q(sender__loginid=uid) & Q(receiver__loginid=usersid)
    | Q(sender__loginid=usersid) & Q(receiver__loginid=uid)
    ).order_by("-timestamp").first()

    if last_message:
        last_message_time = last_message.timestamp
    else:
        last_message_time = None
    
    if request.POST:
        msg = request.POST.get("msg", "")
        image = request.FILES.get("fileInput")
        print("Image", image)
        if image:
            sendMsg = Chat.objects.create(
                sender=sender,
                receiver=receiver,
                content_type="image",
                message=msg,
                file=image,
                date=formatted_date,
                time=formatted_time,
                type="right",
            )
            sendMsg.save()
        if msg:
            sendMsg = Chat.objects.create(
                sender=sender,
                receiver=receiver,
                content_type="text",
                message=msg,
                date=formatted_date,
                time=formatted_time,
                type="right",
            )
            sendMsg.save()

    return render(
        request,
        "User/messages.html",
        {"profiles": profile, "pro": receiver, "chatData": chatData,"semail": sender.email,"last_message_time":last_message_time},
    )


def sdel(request):
    abc = Chat.objects.all().delete()
    return HttpResponse("SUCCESS")


def delete_post(request):
    post_id=request.GET.get('pid')
    post=Posts.objects.filter(id=post_id).delete()
    
    return HttpResponse(f"<script>alert('Post Deleted'); window.location= '/profile'</script>")




def add_to_friend_list(request):
    uid=request.session['uid']
    current_user=Userreg.objects.get(loginid=uid)
    userid = request.GET.get('uid') 
    if userid:
        
        user_to_add = Userreg.objects.get(loginid=userid)  # Get the user you want to add as a friend
         # Assuming you are using Django's built-in User model for authentication

        # Check if the friendship already exists
        if Friends_list.objects.filter(user=current_user, friend=user_to_add).exists():
            # Friendship exists, delete it
            Friends_list.objects.filter(user=current_user, friend=user_to_add).delete()
            return HttpResponse(f"<script>alert('Remmoved from Friend list'); window.location= '/users_profile?uid={userid}'</script>")
        else:
            # Friendship doesn't exist, create it
            friendship = Friends_list(user=current_user, friend=user_to_add)
            friendship.save()
            return HttpResponse(f"<script>alert('Added to Friend list'); window.location= '/users_profile?uid={userid}'</script>")
            

def adm_view_user_profile(request):
    userid = request.GET.get("uid")
    Uid = Userreg.objects.get(loginid=userid)
    view = Userreg.objects.filter(loginid=userid)
    
    #view Post
    view_post = Posts.objects.filter(uid=Uid)
    
    
    return render(request,"admin/view_user_profile.html",{"userprofile": view, "posts": view_post})
def out(request):
    # userid = request.GET.get("uid")
    # Uid = Userreg.objects.get(loginid=userid)
    # view = Userreg.objects.filter(loginid=userid)
    
    # #view Post
    # view_post = Posts.objects.filter(uid=Uid)
    
    data=Posts.objects.filter(status="bad")
    print(data)
    return render(request,"admin/out.html",{"data": data})

def my_profile(request):
    user_id = request.session.get("uid")

    user = Userreg.objects.get(loginid=user_id)
    posts = Posts.objects.filter(uid=user).order_by("-id")

    for p in posts:
        p.like_count = Like.objects.filter(pid=p).count()
        p.comment_count = Comments_on_Posts.objects.filter(pid=p).count()
        p.comments = Comments_on_Posts.objects.filter(pid=p)

    return render(request, "User/my_profile.html", {
        "user": user,
        "posts": posts
    })
from django.shortcuts import redirect, get_object_or_404

def delete_post(request, id):
    user_id = request.session.get("uid")

    post = get_object_or_404(Posts, id=id)

    # सुरक्षा: only owner can delete
    if post.uid.loginid.id == user_id:
        post.delete()

    return redirect('my_profile')

# def test():
#     dataset_path = 'Dataset 1.csv'
#     df = pd.read_csv(dataset_path)

#     # Separate features and labels
#     X = df['Text'].astype(str)
#     y = df['Suicide']

#     # Tokenize and pad sequences
#     max_words = 10000
#     max_len = 500
#     tokenizer = Tokenizer(num_words=max_words)
#     tokenizer.fit_on_texts(X)
#     X_seq = tokenizer.texts_to_sequences(X)
#     X_pad = pad_sequences(X_seq, maxlen=max_len)

#     # Split the data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.2, random_state=42)

#     # Build the CNN model
#     model = Sequential()
#     model.add(Embedding(max_words, 50, input_length=max_len))
#     model.add(Conv1D(128, 5, activation='relu'))
#     model.add(GlobalMaxPooling1D())
#     model.add(Dense(64, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(1, activation='sigmoid'))

#     # Compile the model
#     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#     # Train the model
#     model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

#     # Evaluate the model
#     loss, accuracy = model.evaluate(X_test, y_test)
#     print(f'Test Accuracy: {accuracy}')

#     # Make predictions
#     # Replace 'your_text' with the actual text you want to classify
#     new_texts = ["@dizzyhrvy that crap took me forever to put together. iÃ¢Â€Â™m going to go sleep for DAYS"]
#     # new_texts=["kill me now"]
#     new_texts_seq = tokenizer.texts_to_sequences(new_texts)
#     new_texts_pad = pad_sequences(new_texts_seq, maxlen=max_len)
#     predictions = model.predict(new_texts_pad)

#     # Convert predictions to labels
#     predicted_labels = ["suicidal" if pred > 0.5 else "non-suicidal" for pred in predictions]
#     print(f'Predicted Labels+++++++++++++++++++++++++++++++++: {predicted_labels}')
#     if predicted_labels=="suicidal":
#         messages.success(request, "<script>alert('cannot post this')</script>")
#         return redirect("/user_home")
    
# test()
