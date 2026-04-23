from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password 
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate,login
from .models import *

def index(request):
    return render(request,'index.html')

def adminhome(request):
    return render(request,'admin/adminhome.html')
def buyerhome(request):
    return render(request,'buyer/buyerhome.html')
def farmerhome(request):
    return render(request,'farmer/farmerhome.html')

def governmentofficerhome(request):
    return render(request,'governmentofficer/governmentofficerhome.html')

def deliveryboyhome(request):
    return render(request,'deliveryboy/deliveryboyhome.html')

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Login, Farmer

import re
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def farmer_register(request):

    if request.method == 'POST':

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        address = request.POST['address']
        image = request.FILES.get('profile_pic')

        if not re.match(r'^[a-z0-9._%+-]+@gmail\.(com|in)$', email):
            messages.error(request,'Email must be gmail.com or gmail.in')
            return redirect('farmer_register')

        if not re.match(r'^[0-9]{10}$', phone):
            messages.error(request,'Phone number must be 10 digits')
            return redirect('farmer_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('farmer_register')

        if Farmer.objects.filter(phone=phone).exists():
            messages.error(request,'Phone number already exists')
            return redirect('farmer_register')

        login = Login.objects.create(
            username=email,
            email=email,
            first_name=fname,
            last_name=lname,
            usertype='farmer',
            is_active=False,
            viewpassword=password,
            password=make_password(password)
        )

        Farmer.objects.create(
            login=login,
            full_name=fname + ' ' + lname,
            phone=phone,
            address=address,
            profile_pic=image
        )

        messages.success(request,'Registration Successful. Wait for admin approval.')
        return redirect('/login')

    return render(request,'farmer_register.html')

from .models import Buyer
import re
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def buyer_register(request):

    if request.method == 'POST':

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if not re.match(r'^[a-z0-9._%+-]+@gmail\.(com|in)$', email):
            messages.error(request,'Email must be gmail.com or gmail.in')
            return redirect('buyer_register')

        if not re.match(r'^[0-9]{10}$', phone):
            messages.error(request,'Phone number must be 10 digits')
            return redirect('buyer_register')

        if Login.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('buyer_register')

        if Buyer.objects.filter(phone=phone).exists():
            messages.error(request,'Phone number already exists')
            return redirect('buyer_register')

        login = Login.objects.create(
            username=email,
            email=email,
            first_name=fname,
            last_name=lname,
            usertype='buyer',
            is_active=True,
            viewpassword=password,
            password=make_password(password)
        )

        Buyer.objects.create(
            login=login,
            full_name=fname + ' ' + lname,
            phone=phone
        )

        messages.success(request,'Buyer Registration Successful')
        return redirect('/login')

    return render(request,'buyer_register.html')


def adm(request):
    adm=Login.objects.create_superuser(username='admin',email='admin@gmail.com',viewpassword='admin',password='admin',usertype='admin')
    adm.save()
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                messages.error(request, 'Your account is not approved yet')
                return redirect('login')

            login(request, user)

            # ✅ store session id
            request.session['uid'] = user.id
            request.session['usertype'] = user.usertype

            if user.usertype == 'admin':
                messages.success(request,'Login successful as Admin')
                return redirect('adminhome')

            elif user.usertype == 'buyer':
                messages.success(request,'Login successful as Buyer')
                return redirect('buyerhome')

            elif user.usertype == 'farmer':
                messages.success(request,'Login successful as Farmer')
                return redirect('farmerhome')
            
            elif user.usertype == 'officer':
                messages.success(request,'Login successful as Government Officer')
                return redirect('governmentofficerhome')
            
            elif user.usertype == 'delivery':
                messages.success(request,'Login successful as Delivery Boy')
                return redirect('deliveryboyhome')

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


def admin_farmers(request):
    farmers = Farmer.objects.select_related('login').order_by('-created_at')
    return render(request, 'admin/admin_farmers.html', {'farmers': farmers})

def approve_farmer(request, id):
    farmer = Farmer.objects.get(id=id)
    farmer.login.is_active = True
    farmer.login.save()
    messages.success(request, f'Farmer {farmer.full_name} has been approved.')
    return redirect('admin_farmers')

def reject_farmer(request, id):
    farmer = Farmer.objects.get(id=id)
    farmer.login.delete()
    farmer.delete()
    messages.success(request, f'Farmer {farmer.full_name} has been rejected and removed.')
    return redirect('admin_farmers')

def admin_buyers(request):
    buyers = Buyer.objects.select_related('login').order_by('-created_at')
    return render(request, 'admin/admin_buyers.html', {'buyers': buyers})


def reject_buyer(request, id):
    buyer = Buyer.objects.get(id=id)
    buyer.login.delete()
    buyer.delete()
    messages.success(request, f'Buyer {buyer.full_name} has been rejected and removed.')
    return redirect('admin_buyers')




def farmer_profile(request):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)
    return render(request, 'farmer/farmer_profile.html', {'farmer': farmer})


def edit_farmer_profile(request):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)
    login_user = Login.objects.get(id=uid)

    if request.method == 'POST':
        farmer.full_name = request.POST['full_name']
        farmer.phone = request.POST['phone']
        farmer.address = request.POST['address']
        farmer.save()

        login_user.email = request.POST['email']
        login_user.save()

        return redirect('farmer_profile')

    return render(request, 'farmer/edit_farmer_profile.html', {
        'farmer': farmer,
        'login_user': login_user
    })



def buyer_profile(request):
    uid = request.session.get('uid')
    buyer = Buyer.objects.get(login_id=uid)
    login_user = Login.objects.get(id=uid)

    return render(request, 'buyer/buyer_profile.html', {
        'buyer': buyer,
        'login_user': login_user
    })


def edit_buyer_profile(request):
    uid = request.session.get('uid')
    buyer = Buyer.objects.get(login_id=uid)
    login_user = Login.objects.get(id=uid)

    if request.method == 'POST':
        buyer.full_name = request.POST['full_name']
        buyer.phone = request.POST['phone']
        login_user.email = request.POST['email']

        buyer.save()
        login_user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('buyer_profile')

    return render(request, 'buyer/edit_buyer_profile.html', {
        'buyer': buyer,
        'login_user': login_user
    })



import re
from django.contrib import messages
from django.contrib.auth.hashers import make_password

def admin_add_officer(request):

    if request.method == 'POST':

        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        department = request.POST['department']
        password = request.POST['password']
        image = request.FILES['image']

        if not re.match(r'^[a-z0-9._%+-]+@gmail\.(com|in)$', email):
            messages.error(request,'Email must be gmail.com or gmail.in')
            return redirect('admin_add_officer')

        if not re.match(r'^[0-9]{10}$', phone):
            messages.error(request,'Phone number must be exactly 10 digits')
            return redirect('admin_add_officer')

        if Login.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('admin_add_officer')

        if GovernmentOfficer.objects.filter(phone=phone).exists():
            messages.error(request,'Phone number already exists')
            return redirect('admin_add_officer')

        login_obj = Login.objects.create(
            username=email,
            email=email,
            usertype='officer',
            is_active=True,
            viewpassword=password,
            password=make_password(password)
        )

        GovernmentOfficer.objects.create(
            login=login_obj,
            full_name=full_name,
            phone=phone,
            department=department,
            image=image
        )

        messages.success(request,'Government Officer added successfully')
        return redirect('admin_view_officers')

    return render(request,'admin/add_officer.html')


def admin_view_officers(request):
    officers = GovernmentOfficer.objects.all()
    return render(request, 'admin/view_officers.html', {'officers': officers})


def admin_delete_officer(request, id):
    officer = GovernmentOfficer.objects.get(id=id)
    officer.login.delete()
    officer.delete()
    messages.success(request, 'Officer removed successfully')
    return redirect('admin_view_officers')


def admin_edit_officer(request, id):
    officer = GovernmentOfficer.objects.get(id=id)
    login_user = officer.login

    if request.method == 'POST':
        officer.full_name = request.POST['full_name']
        officer.phone = request.POST['phone']
        officer.department = request.POST['department']

        login_user.email = request.POST['email']
        login_user.username = request.POST['email']

        if 'image' in request.FILES:
            officer.image = request.FILES['image']

        officer.save()
        login_user.save()

        messages.success(request, 'Officer details updated successfully')
        return redirect('admin_view_officers')

    return render(request, 'admin/edit_officer.html', {
        'officer': officer,
        'login_user': login_user
    })


def officer_profile(request):
    uid = request.session.get('uid')
    officer = GovernmentOfficer.objects.get(login_id=uid)

    return render(request, 'governmentofficer/officers_profile.html', {
        'officer': officer
    })

def edit_officer_profile(request):
    uid = request.session.get('uid')
    officer = GovernmentOfficer.objects.get(login_id=uid)
    login_user = officer.login

    if request.method == 'POST':
        officer.full_name = request.POST['full_name']
        officer.phone = request.POST['phone']
        officer.department = request.POST['department']

        login_user.email = request.POST['email']
        login_user.username = request.POST['email']

        if 'image' in request.FILES:
            officer.image = request.FILES['image']

        officer.save()
        login_user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('officer_profile')

    return render(request, 'governmentofficer/edit_officers_profile.html', {
        'officer': officer,
        'login_user': login_user
    })


def officer_add_seeds_fertilisers(request):
    uid = request.session.get('uid')
    officer = GovernmentOfficer.objects.get(login_id=uid)

    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        image = request.FILES['image']

        SeedFertiliser.objects.create(
            officer=officer,
            name=name,
            category=category,
            description=description,
            quantity=quantity,
            price=price,
            image=image
        )
        messages.success(request, 'Product added successfully')
        return redirect('officer_view_seeds_fertilisers')

    return render(request, 'governmentofficer/add_seeds_fertilisers.html')



def officer_view_seeds_fertilisers(request):
    uid = request.session.get('uid')
    officer = GovernmentOfficer.objects.get(login_id=uid)
    products = SeedFertiliser.objects.filter(officer=officer)

    return render(request, 'governmentofficer/view_seeds_fertilisers.html', {
        'products': products
    })


def officer_edit_seeds_fertilisers(request, id):
    product = SeedFertiliser.objects.get(id=id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('officer_view_seeds_fertilisers')

    return render(request, 'governmentofficer/edit_seeds_fertilisers.html', {
        'product': product
    })


def officer_delete_seeds_fertilisers(request, id):
    product = SeedFertiliser.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('officer_view_seeds_fertilisers')


def admin_seeds_fertilisers(request):
    seeds = SeedFertiliser.objects.filter(category='Seed')
    fertilisers = SeedFertiliser.objects.filter(category='Fertiliser')

    return render(request, 'admin/admin_seeds_fertilisers.html', {
        'seeds': seeds,
        'fertilisers': fertilisers
    })


def farmer_view_seeds_fertilisers(request):
    uid = request.session.get('uid')

    farmer = Farmer.objects.get(login_id=uid)

    products = SeedFertiliser.objects.all().order_by('-created_at')

    return render(
        request,
        'farmer/farmer_view_seeds_fertilisers.html',
        {'products': products}
    )


def farmer_add_to_cart(request, pid):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)
    product = SeedFertiliser.objects.get(id=pid)

    qty = int(request.POST['quantity'])

    cart_item = FarmerCart.objects.filter(
        farmer=farmer,
        product=product,
        status='cart'
    ).first()

    if cart_item:
        cart_item.quantity += qty
        cart_item.total_price = cart_item.quantity * product.price
        cart_item.save()
    else:
        FarmerCart.objects.create(
            farmer=farmer,
            product=product,
            quantity=qty,
            total_price=qty * product.price
        )

    return redirect('farmer_cart')
def update_cart_quantity(request, cid):
    cart_item = FarmerCart.objects.get(id=cid)

    qty = int(request.POST['quantity'])
    cart_item.quantity = qty
    cart_item.total_price = qty * cart_item.product.price
    cart_item.save()

    return redirect('farmer_cart')

def delete_cart_item(request, cid):
    FarmerCart.objects.filter(id=cid).delete()
    return redirect('farmer_cart')


def farmer_orders(request):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)

    orders = FarmerCart.objects.filter(
        farmer=farmer
    ).exclude(status='cart').order_by('-created_at')

    return render(
        request,
        'farmer/farmer_orders.html',
        {'orders': orders}
    )



def farmer_cart(request):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)

    cart_items = FarmerCart.objects.filter(farmer=farmer, status='cart')

    grand_total = sum(item.total_price for item in cart_items)

    return render(request, 'farmer/farmer_cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })


def farmer_payment(request):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)

    cart_items = FarmerCart.objects.filter(farmer=farmer, status='cart')

    total_amount = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        # PAYMENT SUCCESS (simulation)

        for item in cart_items:
            product = item.product
            product.quantity -= item.quantity
            product.save()

            item.status = 'paid'
            item.save()

        return redirect('farmerhome')

    return render(request, 'farmer/farmer_payment.html', {
        'total_amount': total_amount
    })



import re
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

def admin_add_delivery_boy(request):

    if request.session.get('usertype') != 'admin':
        return redirect('login')

    if request.method == 'POST':

        name = request.POST['full_name']
        phone = request.POST['phone']
        address = request.POST['address']
        username = request.POST['username']
        password = request.POST['password']

        if not re.match(r'^[a-z0-9._%+-]+@gmail\.(com|in)$', username):
            messages.error(request,'Email must be gmail.com or gmail.in')
            return redirect('admin_add_delivery_boy')

        if not re.match(r'^[0-9]{10}$', phone):
            messages.error(request,'Phone number must be exactly 10 digits')
            return redirect('admin_add_delivery_boy')

        if Login.objects.filter(username=username).exists():
            messages.error(request,'Email already exists')
            return redirect('admin_add_delivery_boy')

        if DeliveryBoy.objects.filter(phone=phone).exists():
            messages.error(request,'Phone number already exists')
            return redirect('admin_add_delivery_boy')

        login = Login.objects.create_user(
            username=username,
            email=username,
            password=password,
            usertype='delivery'
        )

        login.viewpassword = password
        login.save()

        DeliveryBoy.objects.create(
            login=login,
            full_name=name,
            phone=phone,
            address=address
        )

        messages.success(request,'Delivery boy added successfully')
        return redirect('admin_delivery_boy')

    return render(request,'admin/admin_add_delivery_boy.html')

def admin_delivery_boy(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    data = DeliveryBoy.objects.all()
    return render(request, 'admin/admin_delivery_boy.html', {'data': data})


def edit_delivery_boy(request, id):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    boy = get_object_or_404(DeliveryBoy, id=id)

    if request.method == "POST":
        boy.full_name = request.POST.get('full_name')
        boy.phone = request.POST.get('phone')
        boy.address = request.POST.get('address')
        boy.save()

        messages.success(request, 'Delivery boy updated successfully')
        return redirect('admin_delivery_boy')

    return render(
        request,
        'admin/edit_delivery_boy.html',
        {'boy': boy}
    )


def delete_delivery_boy(request, id):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    boy = get_object_or_404(DeliveryBoy, id=id)
    boy.login.delete()
    boy.delete()
    messages.success(request, 'Delivery boy deleted successfully')
    return redirect('admin_delivery_boy')



def deliveryboy_profile(request):
    if request.session.get('usertype') != 'delivery':
        return redirect('login')

    uid = request.session.get('uid')
    boy = get_object_or_404(DeliveryBoy, login_id=uid)

    return render(
        request,
        'deliveryboy/deliveryboy_profile.html',
        {'boy': boy}
    )


def edit_deliveryboy_profile(request):
    if request.session.get('usertype') != 'delivery':
        return redirect('login')

    uid = request.session.get('uid')
    boy = get_object_or_404(DeliveryBoy, login_id=uid)

    if request.method == "POST":
        boy.full_name = request.POST.get('full_name')
        boy.phone = request.POST.get('phone')
        boy.address = request.POST.get('address')
        boy.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('deliveryboy_profile')

    return render(
        request,
        'deliveryboy/edit_deliveryboy_profile.html',
        {'boy': boy}
    )

def admin_assign_delivery(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    orders = FarmerCart.objects.filter(status__in=['paid', 'assigned','delivered'])
    boys = DeliveryBoy.objects.all()

    return render(
        request,
        'admin/admin_assign_delivery.html',
        {
            'orders': orders,
            'boys': boys
        }
    )


def assign_delivery_boy(request, oid):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    order = FarmerCart.objects.get(id=oid)

    if request.method == "POST":
        boy_id = request.POST.get('delivery_boy')
        boy = DeliveryBoy.objects.get(id=boy_id)

        order.delivery_boy = boy
        order.status = 'assigned'
        order.save()

        messages.success(request, 'Delivery boy assigned successfully')
        return redirect('admin_assign_delivery')



def assigned_seeds_fertilisers_deliveryboy(request):
    if request.session.get('usertype') != 'delivery':
        return redirect('login')

    delivery_boy = DeliveryBoy.objects.get(login_id=request.session['uid'])

    active_orders = FarmerCart.objects.filter(
        delivery_boy=delivery_boy,
        status__in=['assigned', 'picked', 'out_for_delivery']
    ).order_by('-created_at')

    delivered_orders = FarmerCart.objects.filter(
        delivery_boy=delivery_boy,
        status='delivered'
    ).order_by('-created_at')

    return render(
        request,
        'deliveryboy/assigned_seeds_fertilisers_deliveryboy.html',
        {
            'active_orders': active_orders,
            'delivered_orders': delivered_orders
        }
    )
def update_seed_delivery_status(request, cid):
    if request.session.get('usertype') != 'delivery':
        return redirect('login')

    delivery_boy = DeliveryBoy.objects.get(login_id=request.session['uid'])
    order = get_object_or_404(
        FarmerCart,
        id=cid,
        delivery_boy=delivery_boy
    )

    if request.method == "POST":
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()
        messages.success(request, "Delivery status updated")

    return redirect('assigned_seeds_fertilisers_deliveryboy')



def deliveryboy_mark_delivered(request, cid):
    if request.session.get('usertype') != 'delivery':
        return redirect('login')

    uid = request.session.get('uid')
    delivery_boy = DeliveryBoy.objects.get(login_id=uid)

    order = get_object_or_404(
        FarmerCart,
        id=cid,
        delivery_boy=delivery_boy,
        status='assigned'
    )

    order.status = 'delivered'
    order.save()

    messages.success(request, 'Order marked as delivered')
    return redirect('assigned_seeds_fertilisers_deliveryboy')


def add_product(request):
    if 'uid' not in request.session:
        return redirect('login')

    farmer = Farmer.objects.get(login_id=request.session['uid'])

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Product.objects.create(
            farmer=farmer,
            product_name=product_name,
            category=category,
            quantity=quantity,
            price=price,
            description=description,
            image=image
        )

        messages.success(request, 'Product added successfully')
        return redirect('view_my_products')

    return render(request, 'farmer/add_products.html')

def view_my_products(request):
    if 'uid' not in request.session:
        return redirect('login')

    farmer = Farmer.objects.get(login_id=request.session['uid'])
    products = Product.objects.filter(farmer=farmer)

    return render(request, 'farmer/view_my_products.html', {'products': products})


def edit_product(request, pid):
    if 'uid' not in request.session:
        return redirect('login')

    product = Product.objects.get(id=pid)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.category = request.POST.get('category')
        product.quantity = request.POST.get('quantity')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('view_my_products')

    return render(request, 'farmer/edit_product.html', {'product': product})


def delete_product(request, pid):
    if 'uid' not in request.session:
        return redirect('login')

    product = Product.objects.get(id=pid)
    product.delete()

    messages.success(request, 'Product deleted successfully')
    return redirect('view_my_products')



def buyer_product_list(request):
    if 'uid' not in request.session:
        return redirect('login')

    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    return render(request, 'buyer/buyer_product_list.html', {'products': products})




def add_to_cart(request, pid):
    if 'uid' not in request.session:
        return redirect('login')

    buyer = Buyer.objects.get(login_id=request.session['uid'])
    product = Product.objects.get(id=pid)

    # Only consider cart items that are still pending
    cart_item = ProductCart.objects.filter(
        buyer=buyer,
        product=product,
        status='pending'
    ).first()

    if cart_item:
        # Check if quantity exceeds product stock
        if cart_item.quantity + 1 > product.quantity:
            messages.error(request, 'Not enough stock available')
            return redirect('buyer_product_list')

        # Increase quantity & total
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.price
        cart_item.save()
        messages.success(request, 'Product quantity updated in cart')
    else:
        if product.quantity < 1:
            messages.error(request, 'Product out of stock')
            return redirect('buyer_product_list')

        ProductCart.objects.create(
            buyer=buyer,
            product=product,
            quantity=1,
            price=product.price,
            total_price=product.price,
            status='pending'
        )
        messages.success(request, 'Product added to cart')

    return redirect('buyer_product_list')



def view_cart(request):
    if 'uid' not in request.session:
        return redirect('login')

    buyer = Buyer.objects.get(login_id=request.session['uid'])

    cart_items = ProductCart.objects.filter(
        buyer=buyer,
        status='pending'
    )

    grand_total = sum(item.total_price for item in cart_items)

    return render(request, 'buyer/view_cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })



def increase_cart_quantity(request, cid):
    cart_item = ProductCart.objects.get(id=cid)
    product = cart_item.product

    if cart_item.quantity + 1 <= product.quantity:
        cart_item.quantity += 1
        cart_item.total_price = cart_item.quantity * cart_item.price
        cart_item.save()
    else:
        messages.error(request, 'Stock limit reached')

    return redirect('view_cart')

def decrease_cart_quantity(request, cid):
    cart_item = ProductCart.objects.get(id=cid)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_price = cart_item.quantity * cart_item.price
        cart_item.save()

    return redirect('view_cart')



def remove_from_cart(request, cid):
    if 'uid' not in request.session:
        return redirect('login')

    cart_item = ProductCart.objects.get(id=cid)
    cart_item.delete()

    messages.success(request, 'Item removed from cart')
    return redirect('view_cart')

def products_payment(request):
    if 'uid' not in request.session:
        return redirect('login')

    buyer = Buyer.objects.get(login_id=request.session['uid'])
    cart_items = ProductCart.objects.filter(buyer=buyer, status='pending')

    grand_total = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        card_no = request.POST.get('card_no')
        holder_name = request.POST.get('holder_name')
        expiry = request.POST.get('expiry')
        cvv = request.POST.get('cvv')

        if card_no and holder_name and expiry and cvv:

            # 🔽 Reduce product stock
            for item in cart_items:
                product = item.product

                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                    product.save()
                else:
                    messages.error(
                        request,
                        f"Insufficient stock for {product.product_name}"
                    )
                    return redirect('view_cart')

            # ✅ Mark cart items as PAID
            cart_items.update(status='paid')

            messages.success(request, 'Payment successful')
            return redirect('buyerhome')

        messages.error(request, 'Invalid card details')

    return render(request, 'buyer/products_payment.html', {
        'grand_total': grand_total
    })



def buyer_product_orders(request):
    if 'uid' not in request.session:
        return redirect('login')

    buyer = Buyer.objects.get(login_id=request.session['uid'])

    orders = ProductCart.objects.filter(
        buyer=buyer,
        status__in=['paid', 'assigned', 'picked', 'out_for_delivery', 'delivered']
    ).order_by('-created_at')

    # 👇 attach feedback flag dynamically
    for o in orders:
        o.feedback_given = ProductFeedback.objects.filter(cart=o).exists()

    return render(request, 'buyer/buyers_product_orders.html', {
        'orders': orders
    })




def admin_products_assign_delivery(request):
    if 'uid' not in request.session or request.session.get('usertype') != 'admin':
        return redirect('login')

    unassigned_carts = ProductCart.objects.filter(
        status='paid',
        delivery_boy__isnull=True
    )

    assigned_carts = ProductCart.objects.filter(
        status='assigned',
        delivery_boy__isnull=False
    )

    delivered_carts = ProductCart.objects.filter(
        status='delivered'
    )

    delivery_boys = DeliveryBoy.objects.all()

    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        delivery_boy_id = request.POST.get('delivery_boy')

        cart = ProductCart.objects.get(id=cart_id)
        delivery_boy = DeliveryBoy.objects.get(id=delivery_boy_id)

        cart.delivery_boy = delivery_boy
        cart.status = 'assigned'
        cart.save()

        messages.success(request, 'Delivery boy assigned successfully')
        return redirect('admin_products_assign_delivery')

    return render(request, 'admin/admin_products_assign_delivery.html', {
        'unassigned_carts': unassigned_carts,
        'assigned_carts': assigned_carts,
        'delivered_carts': delivered_carts,
        'delivery_boys': delivery_boys
    })

def assigned_products_deliveryboy(request):
    if 'uid' not in request.session or request.session.get('usertype') != 'delivery':
        return redirect('login')

    delivery_boy = DeliveryBoy.objects.get(login_id=request.session['uid'])

    active_orders = ProductCart.objects.filter(
        delivery_boy=delivery_boy,
        status__in=['assigned', 'picked', 'out_for_delivery']
    )

    delivered_orders = ProductCart.objects.filter(
        delivery_boy=delivery_boy,
        status='delivered'
    )

    return render(
        request,
        'deliveryboy/assigned_products_deliveryboy.html',
        {
            'active_orders': active_orders,
            'delivered_orders': delivered_orders
        }
    )

def update_delivery_status(request, cart_id):
    if 'uid' not in request.session or request.session.get('usertype') != 'delivery':
        return redirect('login')

    delivery_boy = DeliveryBoy.objects.get(login_id=request.session['uid'])
    cart = ProductCart.objects.get(id=cart_id, delivery_boy=delivery_boy)

    if request.method == "POST":
        new_status = request.POST.get('status')
        cart.status = new_status
        cart.save()
        messages.success(request, "Delivery status updated")

    return redirect('assigned_products_deliveryboy')


# Mark product as delivered
def mark_products_delivered(request, cart_id):
    if 'uid' not in request.session or request.session.get('usertype') != 'delivery':
        return redirect('login')

    delivery_boy = DeliveryBoy.objects.get(login_id=request.session['uid'])
    cart_item = ProductCart.objects.get(id=cart_id, delivery_boy=delivery_boy)

    cart_item.status = 'delivered'
    cart_item.save()

    messages.success(request, f"Order for {cart_item.product.product_name} marked as delivered")
    return redirect('assigned_products_deliveryboy')



def product_feedback(request, cart_id):
    if 'uid' not in request.session:
        return redirect('login')

    buyer = Buyer.objects.get(login_id=request.session['uid'])

    cart = ProductCart.objects.get(
        id=cart_id,
        buyer=buyer,
        status='delivered'
    )

    already_given = ProductFeedback.objects.filter(cart=cart).exists()
    if already_given:
        messages.warning(request, 'Feedback already submitted')
        return redirect('buyer_product_orders')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        if rating and feedback:
            ProductFeedback.objects.create(
                buyer=buyer,
                product=cart.product,
                cart=cart,
                rating=rating,
                feedback=feedback
            )
            messages.success(request, 'Thank you for your feedback')
            return redirect('buyer_product_orders')

        messages.error(request, 'All fields are required')

    return render(request, 'buyer/product_feedback.html', {
        'cart': cart
    })



def farmer_product_feedbacks(request):
    if 'uid' not in request.session or request.session.get('usertype') != 'farmer':
        return redirect('login')

    farmer = Farmer.objects.get(login_id=request.session['uid'])

    feedbacks = ProductFeedback.objects.filter(
        product__farmer=farmer
    ).order_by('-created_at')

    return render(request, 'farmer/farmer_product_feedbacks.html', {
        'feedbacks': feedbacks
    })


def admin_product_feedbacks(request):
    if 'uid' not in request.session or request.session.get('usertype') != 'admin':
        return redirect('login')

    feedbacks = ProductFeedback.objects.all().order_by('-created_at')

    return render(request, 'admin/admin_product_feedbacks.html', {
        'feedbacks': feedbacks
    })


def add_seed_feedback(request, oid):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)

    order = FarmerCart.objects.get(
        id=oid,
        farmer=farmer,
        status='delivered'
    )

    if request.method == "POST":
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        SeedFertiliserFeedback.objects.create(
            farmer=farmer,
            product=order.product,
            order=order,
            rating=rating,
            feedback=feedback
        )

        messages.success(request, 'Feedback submitted successfully')
        return redirect('farmer_orders')

    return render(
        request,
        'farmer/add_seed_feedback.html',
        {'order': order}
    )


def admin_seed_feedback(request):
    if request.session.get('usertype') != 'admin':
        return redirect('login')

    feedbacks = SeedFertiliserFeedback.objects.all().order_by('-created_at')

    return render(
        request,
        'admin/admin_seed_feedback.html',
        {'feedbacks': feedbacks}
    )

def officer_seed_feedback(request):
    if request.session.get('usertype') != 'officer':
        return redirect('login')

    officer = GovernmentOfficer.objects.get(login_id=request.session['uid'])

    feedbacks = SeedFertiliserFeedback.objects.filter(
        product__officer=officer
    ).order_by('-created_at')

    return render(
        request,
        'governmentofficer/officer_seed_feedback.html',
        {'feedbacks': feedbacks}
    )

from datetime import datetime as dt
from django.db.models import Q

def officer_chat(request):
    uid = request.session.get('uid')
    officer = GovernmentOfficer.objects.get(login_id=uid)

    farmers = Farmer.objects.all()
    fid = request.GET.get('id')
    farmer_name = ""

    chats = FarmerOfficerChat.objects.none()

    if fid:
        farmer = Farmer.objects.get(id=fid)
        farmer_name = farmer.full_name

        chats = FarmerOfficerChat.objects.filter(
            Q(officer=officer, farmer=farmer)
        )

    current_time = dt.now().strftime("%H:%M")

    if request.method == "POST":
        message = request.POST.get('message')
        FarmerOfficerChat.objects.create(
            officer=officer,
            farmer=farmer,
            message=message,
            time=current_time,
            sender_type="OFFICER"
        )

    return render(
        request,
        'governmentofficer/chat.html',
        {
            'farmers': farmers,
            'chats': chats,
            'farmer_name': farmer_name,
            'fid': fid
        }
    )


def farmer_chat(request):
    uid = request.session.get('uid')
    farmer = Farmer.objects.get(login_id=uid)

    officers = GovernmentOfficer.objects.all()
    oid = request.GET.get('id')
    officer_name = ""

    chats = FarmerOfficerChat.objects.none()

    if oid:
        officer = GovernmentOfficer.objects.get(id=oid)
        officer_name = officer.full_name

        chats = FarmerOfficerChat.objects.filter(
            Q(farmer=farmer, officer=officer)
        )

    current_time = dt.now().strftime("%H:%M")

    if request.method == "POST":
        message = request.POST.get('message')
        FarmerOfficerChat.objects.create(
            farmer=farmer,
            officer=officer,
            message=message,
            time=current_time,
            sender_type="FARMER"
        )

    return render(
        request,
        'farmer/chat.html',
        {
            'officers': officers,
            'chats': chats,
            'officer_name': officer_name,
            'oid': oid
        }
    )


def add_farming_alert(request):
    if request.session.get('usertype') != 'officer':
        return redirect('login')

    officer = GovernmentOfficer.objects.get(login_id=request.session['uid'])

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        video = request.FILES.get('video')

        FarmingAlert.objects.create(
            officer=officer,
            title=title,
            description=description,
            image=image,
            video=video
        )

        messages.success(request, 'Farming alert published successfully')
        return redirect('view_farming_alerts')

    return render(request, 'governmentofficer/add_farming_alert.html')


def view_farming_alerts(request):
    if request.session.get('usertype') != 'officer':
        return redirect('login')

    officer = GovernmentOfficer.objects.get(login_id=request.session['uid'])
    alerts = FarmingAlert.objects.filter(officer=officer).order_by('-created_at')

    return render(request, 'governmentofficer/view_farming_alerts.html', {
        'alerts': alerts
    })


# EDIT ALERT
def edit_farming_alert(request, alert_id):
    if request.session.get('usertype') != 'officer':
        return redirect('login')

    officer = GovernmentOfficer.objects.get(login_id=request.session['uid'])
    alert = get_object_or_404(FarmingAlert, id=alert_id, officer=officer)

    if request.method == 'POST':
        alert.title = request.POST.get('title')
        alert.description = request.POST.get('description')

        if request.FILES.get('image'):
            alert.image = request.FILES.get('image')

        if request.FILES.get('video'):
            alert.video = request.FILES.get('video')

        alert.save()
        messages.success(request, 'Farming alert updated successfully')
        return redirect('view_farming_alerts')

    return render(request, 'governmentofficer/edit_farming_alert.html', {
        'alert': alert
    })


# DELETE ALERT
def delete_farming_alert(request, alert_id):
    if request.session.get('usertype') != 'officer':
        return redirect('login')

    officer = GovernmentOfficer.objects.get(login_id=request.session['uid'])
    alert = get_object_or_404(FarmingAlert, id=alert_id, officer=officer)

    alert.delete()
    messages.success(request, 'Farming alert deleted successfully')
    return redirect('view_farming_alerts')


def farmer_view_farming_alerts(request):
    if 'uid' not in request.session:
        return redirect('login')

    alerts = FarmingAlert.objects.all().order_by('-created_at')

    return render(request, 'farmer/farmer_view_farming_alerts.html', {
        'alerts': alerts
    })


def admin_products(request):
    if 'uid' not in request.session or request.session.get('usertype') != 'admin':
        return redirect('login')

    products = Product.objects.select_related('farmer', 'farmer__login').order_by('-created_at')

    return render(request, 'admin/admin_products.html', {
        'products': products
    })


import pandas as pd
import joblib
import os
import time
from django.shortcuts import render, redirect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, 'ml', 'crop_disease_model.pkl'))
crop_encoder = joblib.load(os.path.join(BASE_DIR, 'ml', 'crop_encoder.pkl'))
disease_encoder = joblib.load(os.path.join(BASE_DIR, 'ml', 'disease_encoder.pkl'))

df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'crop_disease.csv'))

def predict_crop_disease(request):
    if 'uid' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        crop = request.POST['crop']
        temp = float(request.POST['temperature'])
        humidity = float(request.POST['humidity'])
        soil = float(request.POST['soil'])
        rainfall = float(request.POST['rainfall'])

        # ⏳ Simulate ML processing time (5 seconds)
        time.sleep(5)

        crop_encoded = crop_encoder.transform([crop])[0]

        prediction = model.predict([[crop_encoded, temp, humidity, soil, rainfall]])
        disease = disease_encoder.inverse_transform(prediction)[0]

        suggestion = df[
            (df['Crop'] == crop) & (df['Disease'] == disease)
        ]['Suggestion'].iloc[0]

        return render(request, 'farmer/predict.html', {
            'disease': disease,
            'suggestion': suggestion
        })

    crops = sorted(df['Crop'].unique())
    return render(request, 'farmer/predict.html', {'crops': crops})
