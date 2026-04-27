from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# Create your views here.
def index(request):
    return render(request,"index.html")

def userReg(request):
    msg=''
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        age=request.POST['age']

        otp = get_random_string(length=6, allowed_chars='1234567890')
        try:
            user=CustomUSer.objects.create_user(username=email,password='temperory',is_active=1,usertype="User")
            user.save()
            cust=User.objects.create(name=name,phone=phone,email=email,age=age,address=address,otp=otp,user=user)
            cust.save()
            messages.info(request,"Verify Otp")
            subject = "Your OTP for SMART MATRIX Registration"
            message = f"Hello {name}, your OTP is: {otp}"
            send_mail(subject, message, 'teamlccalwaye@gmail.com', [email])
            request.session['id'] = email
            return redirect('/verify_otpuser')
            # msg="Registration Successfull.."
            # return render(request,"userReg.html",{"msg":msg})
        except:
            msg="Username Already Exists.."
            return render(request,"userReg.html",{"msg":msg})
    else:    
        return render(request,"userReg.html",{"msg":msg})


from django.http import HttpResponse

def verify_otpuser(request):
    username = request.session.get('id')
    print("Session username:", username)

    if not username:
        return redirect('/')

    user = CustomUSer.objects.get(username=username)
    user_detail = User.objects.get(user=user)

    if request.method == 'POST':
        otp_entered = request.POST['otp']
        print("OTP Entered:", otp_entered)
        print("OTP Stored:", user_detail.otp)

        if otp_entered == user_detail.otp:
            generated_password = get_random_string(length=8)
            user.set_password(generated_password)
            user.save()
            print(user.username,"##################################################################################################")
            # user.viewpassword = generated_password
            # user.save()

            user_detail.is_verified = True
            user_detail.save()

            send_mail(
                "Your Password",
                f"Hello {user_detail.name}, your password is: {generated_password}",
                'teamlccalwaye@gmail.com',
                [user.username]
            )

            messages.info(request, "OTP verified. Password sent to email.")
            return redirect("/login")
        else:
            messages.info(request, "Invalid OTP")
            return render(request, 'otp.html', {'error': 'Invalid OTP'})
    
    return render(request, 'otp.html')



def verify_otp(request):
    username = request.session.get('id')
    print("Session username:", username)

    if not username:
        return redirect('/')

    user = CustomUSer.objects.get(username=username)
    user_detail = Shop.objects.get(user=user)

    if request.method == 'POST':
        otp_entered = request.POST['otp']
        print("OTP Entered:", otp_entered)
        print("OTP Stored:", user_detail.otp)

        if otp_entered == user_detail.otp:
            generated_password = get_random_string(length=8)
            user.set_password(generated_password)
            user.save()
            print(user.username,"##################################################################################################")
            # user.viewpassword = generated_password
            # user.save()

            user_detail.is_verified = True
            user_detail.save()

            send_mail(
                "Your Password",
                f"Hello {user_detail.name}, your password is: {generated_password}",
                'teamlccalwaye@gmail.com',
                [user.username]
            )

            messages.info(request, "OTP verified. Password sent to email.")
            return redirect("/login")
        else:
            messages.info(request, "Invalid OTP")
            return render(request, 'otp.html', {'error': 'Invalid OTP'})
    
    return render(request, 'otp.html')

def verify_otpDBoy(request):
    username = request.session.get('id')
    print("Session username:", username)

    if not username:
        return redirect('/')

    user = CustomUSer.objects.get(username=username)
    user_detail = Delivery_boy.objects.get(user=user)

    if request.method == 'POST':
        otp_entered = request.POST['otp']
        print("OTP Entered:", otp_entered)
        print("OTP Stored:", user_detail.otp)

        if otp_entered == user_detail.otp:
            generated_password = get_random_string(length=8)
            user.set_password(generated_password)
            user.save()
            print(user.username,"##################################################################################################")
            # user.viewpassword = generated_password
            # user.save()

            user_detail.is_verified = True
            user_detail.save()

            send_mail(
                "Your Password",
                f"Hello {user_detail.name}, your password is: {generated_password}",
                'teamlccalwaye@gmail.com',
                [user.username]
            )

            messages.info(request, "OTP verified. Password sent to email.")
            return redirect("/login")
        else:
            messages.info(request, "Invalid OTP")
            return render(request, 'otp.html', {'error': 'Invalid OTP'})
    
    return render(request, 'otp.html')

def shopReg(request):
    msg=''
    if request.POST:
        name=request.POST['name']
        owner_name=request.POST['owner_name']
        email=request.POST['email']
        phone=request.POST['phone']
        licence=request.POST['licence']
        address=request.POST['address']
        image=request.FILES['image']
        otp = get_random_string(length=6, allowed_chars='1234567890')
        try: 
            user=CustomUSer.objects.create_user(username=email,password='temperory',is_active=0,usertype="Shop")
            user.save()
            # shop=Shop.objects.create(name=name,owner=owner_name,email=email,phone=phone,address=address,user=user,airport=airport,licence=licence)
            shop=Shop.objects.create(name=name,owner=owner_name,email=email,phone=phone,address=address,otp=otp,user=user,licence=licence,image=image)
            shop.save()
            messages.info(request,"Verify Otp")
            subject = "Your OTP for SMART MATRIX Registration"
            message = f"Hello {name}, your OTP is: {otp}"
            send_mail(subject, message, 'teamlccalwaye@gmail.com', [email])
            request.session['id'] = email
            return redirect('/verify_otp')
            msg="Registration Successfull.."
            return render(request,"shopReg.html",{"msg":msg})
        except:
            msg="Username Already Exists.."
            return render(request,"shopReg.html",{"msg":msg})
    else:
        return render(request,"shopReg.html",{"msg":msg})    
    

def deliveryboyReg(request):
    shops=Shop.objects.all()
    msg=''
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        # password=request.POST['password']
        shop=request.POST['shop']
        proof=request.FILES['proof']
        shopy=Shop.objects.get(id=shop)
        otp = get_random_string(length=6, allowed_chars='1234567890')
        
        try:
            user=CustomUSer.objects.create_user(username=email,password='temperory',is_active=0,usertype="Delivery_boy")
            user.save()
            cust=Delivery_boy.objects.create(name=name,phone=phone,email=email,address=address,user=user,shop=shopy,proof=proof,otp=otp)
            cust.save()
            messages.info(request,"Verify Otp")
            subject = "Your OTP for SMART MATRIX Registration"
            message = f"Hello {name}, your OTP is: {otp}"
            send_mail(subject, message, 'teamlccalwaye@gmail.com', [email])
            request.session['id'] = email
            return redirect('/verify_otpDBoy')
            return render(request,"deliveryboyReg.html",{"msg":msg})
        except:
            msg="Username Already Exists.."
            return render(request,"deliveryboyReg.html",{"msg":msg})
    else:
        return render(request,"deliveryboyReg.html",{"msg":msg,"shop":shops})

def login(request):
    msg=''
    if request.POST:
        username=request.POST['username']
        password=request.POST['password']
        print(password,"###########################################################")
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                return redirect("/adminHome")
            elif user.usertype == 'User':
                data=User.objects.get(email=username)
                if data.is_verified == False:
                    messages.info(request, "OTP not Verified")
                    return redirect("/login")
                request.session['id']=data.id
                return redirect("/userHome")
            elif user.usertype == 'Shop':
                data=Shop.objects.get(email=username)
                if data.is_verified == False:
                    messages.info(request, "OTP not Verified")
                    return redirect("/login")
                request.session['id']=data.id
                return redirect("/shopHome")
            elif user.usertype == 'Delivery_boy':
                data=Delivery_boy.objects.get(email=username)
                request.session['id']=data.id
                return redirect("/deliveryBoyHome")
        else:
            msg="Invalid Username or Password!"
            return render(request,"login.html",{"msg":msg})
    return render(request,"login.html",{"msg":msg})

def adminHome(request):
    return render(request,"adminHome.html")

def adminUser(request):
    data=User.objects.all().order_by("-id")
    return render(request,"adminUser.html",{"data":data})

def adminSupplier(request):
    data=Shop.objects.all().order_by("-id")
    return render(request,"adminSupplier.html",{"data":data})

def adminApproveShop(request):
    id=request.GET['id']
    status=request.GET['status']
    data=CustomUSer.objects.get(id=id)
    data.is_active=status
    data.save()
    return redirect("/adminSupplier")


def adminDelivery(request):
    data=Delivery_boy.objects.all().order_by("-id")
    return render(request,"adminDelivery.html",{"data":data})


def adminApproveDelivery(request):
    id=request.GET['id']
    status=request.GET['status']
    data=CustomUSer.objects.get(id=id)
    data.is_active=status
    data.save()
    return redirect("/adminDelivery")

def adminProduct(request):
    pro=Products.objects.all().order_by("-id")
    return render(request,"adminProduct.html",{"pro":pro})

def adminFeedback(request):
    pro=Feedback.objects.all().order_by("-id")
    return render(request,"adminFeedback.html",{"pro":pro})

def adminReport(request):
    selected_month = request.GET.get('month', '')
    selected_type = request.GET.get('type', '').strip()
    selected_shop = request.GET.get('shop', '')

    bok = Bookings.objects.filter().exclude(status='CART').order_by("-id")
    shops = Shop.objects.all().order_by('name')

    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))
            bok = bok.filter(book_date__year=year, book_date__month=month)
        except ValueError:
            return render(
                request,
                "adminReport.html",
                {
                    "bok": bok,
                    "error": "Invalid month format",
                    "selected_month": selected_month,
                    "selected_type": selected_type,
                    "selected_shop": selected_shop,
                    "growth_total_price": sum(b.total for b in bok),
                    "shops": shops,
                },
            )

    if selected_type:
        bok = bok.filter(Product__type__icontains=selected_type)

    if selected_shop:
        bok = bok.filter(Product__user_id=selected_shop)

    total_price = sum(b.total for b in bok)
    return render(
        request,
        "adminReport.html",
        {
            "bok": bok,
            "selected_month": selected_month,
            "selected_type": selected_type,
            "selected_shop": selected_shop,
            "growth_total_price": total_price,
            "shops": shops,
        },
    )


def adminSalaryReport(request):
    salary = Salary.objects.filter().order_by("-date")
    total_earnings = sum(s.amount or 0 for s in salary)
    return render(request, "adminSalaryReport.html", {"salary": salary, "total_earnings": total_earnings})
    

# def userHome(request):
#     return render(request,"userHome.html")








# from .recommender import recommend_products

# def userHome(request):
#     uid = request.session.get('id')

#     recommended = []
#     if uid:
#         recommended = recommend_products(uid)

#     return render(request, "userHome.html", {
#         "recommended": recommended
#     })







# from .recommender import recommend_products

# def userHome(request):
#     uid = request.session.get('id')

#     recommended = []

#     if uid:
#         recommended = list(recommend_products(uid))

#         # 🔁 Fallback: if no recommendations left
#         if not recommended:
#             recommended = Products.objects.order_by('-qty')[:6]
#     else:
#         # Guest user fallback
#         recommended = Products.objects.order_by('-qty')[:6]

#     return render(request, "userHome.html", {
#         "recommended": recommended
#     })






from django.shortcuts import render
# from .recommender import recommend_products
from .models import Products, Bookings

def userHome(request):
    
    return render(request, "userHome.html")




# def userProducts(request):
#     pro = Products.objects.filter().order_by("-id")  # Filter products
#     # pro = Products.objects.filter(datetime__isnull=False, datetime__lt=timezone.now())  # Filter products

#     uid = request.session['id']
#     user = User.objects.get(id=uid)

#     for i in pro:
#         i.discounted_price = int(float(i.price) - (float(i.price) * 0.10))
#         i.discount = int((float(i.price) * 0.10) )


#     if request.POST:
#         pid = request.POST['pid']
#         count = int(request.POST['count']) 
#         prod = Products.objects.get(id=pid)

#         bok = Bookings.objects.filter(cust_id=uid, Product_id=prod, status="CART").first()

#         if bok:  
#             bok.count += count  
#             bok.total = int(prod.price) * bok.count 
#             bok.save()  

           

#             messages.info(request, "Product quantity updated in cart.")
#             return redirect("/userProducts")

#         else:  
#             bok = Bookings.objects.create(
#                 cust=user,
#                 Product=prod,
#                 count=count,
#                 total=int(prod.price) * count
#             )
#             bok.save()

            

#             messages.info(request, "Product Added to Cart.")
#             return redirect("/userProducts")

#     return render(request, "userProducts.html", {"pro": pro})




import pandas as pd
from django.db.models import Q
import os
from django.conf import settings

def userProducts(request):
    pro = Products.objects.all().order_by("-id")

    uid = request.session['id']
    user = User.objects.get(id=uid)

    # ✅ LOAD CSV
    file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'recipes_dataset.csv')

    if not os.path.exists(file_path):
        print("❌ CSV FILE NOT FOUND:", file_path)

    df = pd.read_csv(file_path)

    recommended_products = []
    search_query = request.GET.get('search')

    # 🚫 IGNORE COMMON WORDS (VERY IMPORTANT)
    ignore_words = [
        "spices", "water", "pepper", "gravy",
        "masala", "sauce", "butter"
    ]

    # 🔥 SEARCH LOGIC
    if search_query:
        search = search_query.lower().strip()
        print("🔍 Searching for:", search)

        # MATCH RECIPE NAME
        # recipe = df[df['name'].str.lower().str.contains(search, na=False)]

        # SPLIT USER INPUT (e.g. "chicken biriyani" → ["chicken", "biriyani"])
        words = search.split()
        
        # CREATE EMPTY FILTER
        recipe = df.copy()
        
        for word in words:
            recipe = recipe[recipe['name'].str.lower().str.contains(word, na=False)]

        if not recipe.empty:
            ingredients = recipe.iloc[0]['ingredients'].lower().split(',')
            print("🍛 Ingredients:", ingredients)

            query = Q()

            for item in ingredients:
                item = item.strip()

                # 🚫 SKIP COMMON WORDS
                if item in ignore_words:
                    continue

                # HANDLE PLURAL (vegetables -> vegetable)
                singular = item[:-1] if item.endswith('s') else item

                query |= (
                    Q(name__icontains=item) |
                    Q(name__icontains=singular) |
                    Q(type__icontains=item) |
                    Q(type__icontains=singular)
                )

            recommended_products = Products.objects.filter(query).distinct()

            print("✅ Found products:", recommended_products.count())

        else:
            print("❌ No recipe found in CSV")

    # 💰 DISCOUNT
    for i in pro:
        i.discounted_price = int(float(i.price) - (float(i.price) * 0.10))
        i.discount = int((float(i.price) * 0.10))

    for i in recommended_products:
        i.discounted_price = int(float(i.price) - (float(i.price) * 0.10))

    # 🛒 CART (UNCHANGED)
    if request.method == "POST":
        pid = request.POST['pid']
        count = int(request.POST['count'])
        prod = Products.objects.get(id=pid)

        bok = Bookings.objects.filter(
            cust_id=uid,
            Product_id=prod,
            status="CART"
        ).first()

        if bok:
            bok.count += count
            bok.total = int(prod.price) * bok.count
            bok.save()
        else:
            Bookings.objects.create(
                cust=user,
                Product=prod,
                count=count,
                total=int(prod.price) * count
            )

        return redirect("/userProducts")

    return render(request, "userProducts.html", {
        "pro": pro,
        "recommended_products": recommended_products,
        "search_query": search_query
    })


from django.utils import timezone

def userPreBook(request):
    uid=request.session['id']
    user=User.objects.get(id=uid)
    pro = Products.objects.filter(datetime__isnull=False, datetime__gte=timezone.now()).order_by("-id")

    for i in pro:
        i.discounted_price = int(float(i.price) - (float(i.price) * 0.10))
        i.discount = int((float(i.price) * 0.10) )
        


    if request.POST:
        pid=request.POST['pid']
        count=request.POST['count']
        return redirect(f"/userPrePay?pid={pid}&count={count}")
    
       

    return render(request, "userPreBook.html", {"pro": pro})





def userPrePay(request):
    uid = request.session['id']
    user = User.objects.get(id=uid)
    pid = request.GET['pid']
    count = int(request.GET['count'])  

    prod = Products.objects.get(id=pid)

    discounted_price = int(float(prod.price) - (float(prod.price) * 0.10))


    total_rate = discounted_price * count  

    if request.POST:
        messages.info(request, "Booking Successful.")
        bok = Bookings.objects.create(cust=user, Product=prod, count=count, total=total_rate)
        bok.status="Booked"
        bok.save()

        prod.qty -= count
        prod.save()
        return redirect("/userBookings")

    return render(request, "userPrePay.html", {"rate": total_rate, "discounted_price": discounted_price, "prod": prod, "count": count})





def userCart(request):
    uid=request.session['id']
    data=Bookings.objects.filter(cust__id=uid,status="CART").order_by("-id")
    rate=0
    for i in data:
        rate=rate + int(i.total)
    return render(request,"userCart.html",{"data":data,"rate":rate})

def userRemove(request):
    bid=request.GET['id']
    data=Bookings.objects.get(id=bid)
    data.delete()
    return redirect("/userCart")

    

from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Payment, Bookings, User
from .utils import encrypt_data

def custPay(request):
    if 'id' not in request.session:
        return redirect("/login")

    uid = request.session['id']
    bok = Bookings.objects.filter(cust__id=uid, status="CART")
    rate = 0

    for i in bok:
        rate += int(i.total)

    if request.method == "POST":
        card_number = request.POST.get("card_number")
        exp_month = request.POST.get("exp_month")
        exp_year = request.POST.get("exp_year")
        cvv = request.POST.get("cvv")

        expiry = f"{exp_month}/{exp_year}"

        print("DEBUG DATA:", card_number, exp_month, exp_year, cvv)

        if not all([card_number, exp_month, exp_year, cvv]):
            messages.error(request, "All fields are required!")
            return redirect("/custPay")

        try:
            # 🔐 Encrypt ONCE
            enc_card = encrypt_data(card_number)
            enc_expiry = encrypt_data(expiry)
            enc_cvv = encrypt_data(cvv)

            user = User.objects.get(id=uid)

            # 🔥 IMPORTANT: LOOP BOOKINGS
            for i in bok:
                print("BOOKING ID:", i.id)   # DEBUG

                # 💾 Create payment per booking
                Payment.objects.create(
                    user=user,
                   booking=i,   # ✅ THIS IS THE KEY FIX
                    card_number=enc_card,
                    expiry=enc_expiry,
                    cvv=enc_cvv,
                    amount=i.total   # ✅ per booking amount
                )
                print("PAYMENT CREATED FOR:", i.id)  # DEBUG

                # 🛒 Update booking
                i.status = "Booked"
                i.payment_date = timezone.now()
                i.Product.qty -= i.count
                i.Product.save()
                i.save()

            messages.success(request, "Payment Successful!")
            return redirect("/userBookings")

        except Exception as e:
            print("ERROR:", e)
            messages.error(request, "Payment Failed!")
            return redirect("/custPay")

    return render(request, "userPay.html", {"rate": rate})

def userBookings(request):
    uid=request.session['id']
    bok=Bookings.objects.filter(cust__id=uid).order_by("-id")
    return render(request,"userBookings.html",{"bok":bok})

from django.shortcuts import render, redirect
from .models import Payment
from .utils import decrypt_data

def viewPayment(request):
    if 'id' not in request.session:
        return redirect("/login")

    uid = request.session['id']

    payments = Payment.objects.filter(user__id=uid).select_related("booking")

    data = []

    for p in payments:
        try:
            product_name = "N/A"

            # ✅ SAFE CHECK
            if p.booking and p.booking.Product:
                product_name = p.booking.Product.name

            data.append({
                "product": product_name,
                "card_number": decrypt_data(p.card_number),
                "expiry": decrypt_data(p.expiry),
                "cvv": decrypt_data(p.cvv),
                "amount": p.amount,
                "date": p.created_at
            })

        except Exception as e:
            print("ERROR:", e)

    return render(request, "viewPayment.html", {"payments": data})

def userChat(request):
    bid = request.GET['id']
    book = Bookings.objects.get(id=bid)
    chat=Chat.objects.filter(book=book)
    month = datetime.now()
    month=month.strftime("%B")+month.strftime("%Y")+month.strftime("%U")

    try:
        if request.POST:
            message = request.POST['message']
            image = request.FILES['image']
            chat_add = Chat.objects.create(message=message,book=book,file=image,sender="User",month=month)
            chat_add.save()
            return render(request,"userChat.html",{"chat":chat})
    except:
        if request.POST:
            message = request.POST['message']
            chat_add = Chat.objects.create(message=message,book=book,sender="User",month=month)
            chat_add.save()
            return render(request,"userChat.html",{"chat":chat})
        chat=Chat.objects.filter(book__id=bid)
    return render(request,"userChat.html",{"chat":chat})

def userFeedback(request):
    uid=request.session['id']
    user=User.objects.get(id=uid)
    id=request.GET['id']
    bok=Bookings.objects.get(id=id)
    if request.POST:
        feedback=request.POST['feedback']
        rating = request.POST["rating"]
        feed=Feedback.objects.create(user=user,review=feedback,rating=rating,book=bok)
        feed.save()
        bok.status="Feedback completed"
        bok.save()
        messages.info(request,"Feedback Added Successfully")
        return redirect("/userBookings")
    return render(request,"userFeedback.html")


def shopHome(request):
    return render(request,"shopHome.html")


from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Products, Shop

def shopAdd(request):
    uid = request.session['id']
    shop = Shop.objects.get(id=uid)
    data = Products.objects.filter(user__id=uid).order_by("-id")

    # for product in data:
    #     product.show_original_price = product.datetime and product.datetime < now()

    if request.method == "POST":
        name = request.POST['name']
        type = request.POST['type']
        qty = request.POST['qty']
        price = request.POST['price']
        desc = request.POST['desc']
        discountprice = request.POST['discountprice']
        img = request.FILES['img']
        # fname=request.POST['fname']
        # fnumber=request.POST['fnumber']

        # pro = Products.objects.create(
        #     name=name, type=type, desc=desc, price=price, qty=qty, 
        #     image=img, user=shop, datetime=datetime,fname=fname,fnumber=fnumber
        # )
        pro = Products.objects.create(
            name=name, type=type, desc=desc, price=price, qty=qty, 
            image=img, user=shop, discountprice = discountprice)
        pro.save()

        messages.info(request, "Product Added Successfully..")
        return redirect("/shopAdd")

    return render(request, "shopAdd.html", {"data": data})




def shopAddCount(request):
    if request.POST:
        pid=request.POST['pid']
        count=request.POST['count']
        pro=Products.objects.get(id=pid)
        pro.qty=int(pro.qty)+int(count)
        pro.save()
        return redirect("/shopAdd")
    return render(request,"shopAdd.html")


def shopDelProd(request):
    id = request.GET.get('id')
    prod=Products.objects.get(id=id)
    prod.delete()
    return redirect("/shopAdd")




def shopBooking(request):
    uid=request.session['id']
    bok=Bookings.objects.filter(Product__user__id = uid ).order_by("-id")
    boy=Delivery_boy.objects.filter(shop__id=uid)

    if request.POST:
        name=request.POST['boy']
        bid=request.POST['bid']
        book=Bookings.objects.get(id=bid)
        assigned_boy=Delivery_boy.objects.get(id=name)
        book.boy=assigned_boy
        book.status="Assigned"
        book.save()
    return render(request,"shopBooking.html",{"bok":bok,"boy":boy})

def shopChat(request):
    pid = request.GET['oid']
    order = Bookings.objects.get(id=pid)
    chat = Chat.objects.filter(book = order)
    month = datetime.now()
    month=month.strftime("%B")+month.strftime("%Y")+month.strftime("%U")

    try:
        if request.POST:
            message = request.POST['message']
            image = request.FILES['image']
            chat_add = Chat.objects.create(message=message,book=order,file=image,sender="Shop",month=month)
            chat_add.save()
            return render(request,"shopChat.html",{"chat":chat})
    except:
        if request.POST:
            message = request.POST['message']
            chat_add = Chat.objects.create(message=message,book=order,sender="Shop",month=month)
            chat_add.save()
            return render(request,"shopChat.html",{"chat":chat})
        chat=Chat.objects.filter(book__id=pid)
    return render(request,"shopChat.html",{"chat":chat})




from django.utils.dateparse import parse_date



def shopReport(request):
    uid = request.session['id']
    selected_month = request.GET.get('month', '')
    selected_type = request.GET.get('type', '').strip()

    bok = Bookings.objects.filter(Product__user__id=uid).exclude(status='CART').order_by("-id")
    
    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))
            bok = bok.filter(book_date__year=year, book_date__month=month)
        except ValueError:
            return render(request, "shopReport.html", {"bok": bok, "error": "Invalid month format", "selected_month": selected_month, "selected_type": selected_type})

    if selected_type:
        bok = bok.filter(Product__type__icontains=selected_type)
    
    total_price = sum(b.total for b in bok)
    return render(request, "shopReport.html", {"bok": bok, "selected_month": selected_month, "selected_type": selected_type, "growth_total_price": total_price})




def shopFeedbacks(request):
    uid = request.session['id']
    
    pro=Feedback.objects.filter(book__Product__user_id=uid).order_by("-id")
    return render(request,"shopFeedbacks.html",{"pro":pro})

def shopDBoys(request):
    uid = request.session['id']
    shop = Shop.objects.get(id=uid)

    if request.method == 'POST':
        boy_id = request.POST.get('delivery_boy')
        salary_value = request.POST.get('salary')

        try:
            boy = Delivery_boy.objects.get(id=boy_id, shop=shop)
            salary_amount = int(salary_value)
            Salary.objects.create(boy=boy, shop=shop, amount=salary_amount)
            messages.success(request, f"Salary paid ₹{salary_amount} to {boy.name}.")
            return redirect("/shopDBoys")
        except (Delivery_boy.DoesNotExist, ValueError):
            messages.error(request, "Invalid delivery boy or amount.")

    dboys = Delivery_boy.objects.filter(shop=shop).order_by("-id")
    salaries = Salary.objects.filter(shop=shop).order_by("-date")
    salary_total = sum(s.amount or 0 for s in salaries)
    return render(request, "shopDBoys.html", {"dboys": dboys, "salaries": salaries, "salary_total": salary_total})


def deliveryBoyHome(request):
    return render(request,"deliveryBoyHome.html")



def deliveryOrder(request):
    uid=request.session['id']
    bok=Bookings.objects.filter(boy__id=uid,status="Assigned").order_by("-id")
    return render(request,"deliveryOrder.html",{"bok":bok})


def deliveryUpdate(request):
    uid=request.session['id']
    id=request.GET['id']
    bok=Bookings.objects.get(id=id)
    boy=Delivery_boy.objects.get(id=uid)
    bok.status="Completed"
    boy.status="Completed"
    bok.save()
    boy.save()
    return redirect("/deliveyCompleted")

def deliveyCompleted(request):
    uid=request.session['id']
    bok=Bookings.objects.filter(boy_id=uid,status="Completed").order_by("-id")
    return render(request,"deliveyCompleted.html",{"bok":bok})


def deliveyEarnings(request):
    uid=request.session['id']
    salary = Salary.objects.filter(boy_id=uid).order_by("-date")
    total_earnings = sum(s.amount or 0 for s in salary)
    return render(request, "deliveryEarnings.html", {"salary": salary, "total_earnings": total_earnings})