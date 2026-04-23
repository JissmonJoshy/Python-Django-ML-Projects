from django.shortcuts import render,redirect
from.models import*
from django.contrib import messages
from django.contrib.auth.hashers import check_password
# import MySQLdb
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plot
import numpy as np
import requests
from keras.models import Sequential
from keras.layers import Dense
from sklearn.svm import SVR
import csv
from django.core.files.storage import *

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
# Create your views here.
def home(request):
    return render(request,'index.html')


def login(request):
    return render(request,"user/login.html")

def userreg(request):
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if UserReg.objects.filter(email=email).exists():
            messages.info(request,"email allready exist")
        else:
            user = Login.objects.create(email=email, password=password, userType='user')
            regs = UserReg.objects.create(user=user,name=name,email=email,password=password)
            regs.save()
            messages.info(request,"Register Sucessfully")
        return redirect('/login')
    else:
        return render(request,'user/register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = Login.objects.filter(email=email, password=password).first()

        if user:
            if email == 'admin@gmail.com' and password == 'Admin@123':
                messages.success(request, 'Welcome to Admin Home')
                return redirect('/adminbase')

            elif user.userType == 'user':
                try:
                    userdata = UserReg.objects.get(email=email)
                    if userdata.status == 'Approved':  
                        request.session['uid'] = userdata.id
                        messages.success(request, 'Welcome to User Home')
                        return redirect('/userhome')
                    else:
                        messages.warning(request, 'Your account is not approved yet.')
                        return redirect('/login')
                except UserReg.DoesNotExist:
                    messages.error(request, 'User not found. Please contact support.')
                    return redirect('/login')

            else:
                messages.error(request, 'Invalid user type.')
                return redirect('/login')

        else:
            messages.error(request, 'Invalid email or password. Please try again.')
            return redirect('/login')

    return render(request, 'user/login.html')

def userhome(request):
    return render(request,'user/userhome.html')

def display_users(request):
    users = UserReg.objects.all()
    return render(request, "user/display_users.html", {"users": users})

def approve_user(request, user_id):
    user = UserReg.objects.get(id=user_id)
    user.status = "Approved"
    user.save()
    return redirect("display_users")

def reject_user(request, user_id):
    user = UserReg.objects.get(id=user_id)
    user.status = "Rejected"
    user.save()
    return redirect("display_users")

def delete_user(request, user_id):
    user = UserReg.objects.get(id=user_id)
    if user.user:
        user.user.delete() 
    user.delete()  
    return redirect("display_users")


##########      FIXED INCOME     ################


def fixedincome(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    if request.POST:
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']
        frequency = request.POST['frequency']
        
        fix = FixedIncome.objects.create(
            user_id=uid,
            source=source,
            amount=amount,
            date=date,
            frequency=frequency
        )
        messages.info(request,"successfully Added")
        fix.save()
        return redirect('/fixed_list')
    
    return render(request, 'user/fixedincome.html')

def fixed_list(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    infixed = FixedIncome.objects.filter(user_id=uid)
    return render(request, 'user/fixedlist.html', {'infixed': infixed})
def adminbase(request):
    
   
    return render(request, 'user/Admin_base.html')
def userlist(request):
    
    infixed = UserReg.objects.all()
    return render(request, 'user/userlist.html', {'infixed': infixed})

def updatein(request):
    id = request.GET.get('id')
    infixed = FixedIncome.objects.filter(id=id).first()

    if request.method == "POST":
        infixed.source = request.POST['source']
        infixed.amount = request.POST['amount']
        infixed.date = request.POST['date']
        infixed.frequency = request.POST['frequency']
        infixed.save()

        messages.info(request, "Updated Successfully")
        return redirect('/fixed_list')

    return render(request, "user/fixedincome.html", {'infixed': infixed})

def delete(request):
    id = request.GET.get('id')
    delete = FixedIncome.objects.filter(id=id).delete()
    messages.info(request,"sucessfully Deleted")
    return redirect('/fixed_list')

##########      OTHER INCOME     ################

def otherincome(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    if request.POST:
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']
        frequency = request.POST['frequency']
        
        otrexp = OtherIncome.objects.create(
            user_id=uid,
            source=source,
            amount=amount,
            date=date,
            frequency=frequency
        )
        messages.info(request,"successfully Added")
        otrexp.save()
        return redirect('/fixed_list')
    
    return render(request, 'user/otherincome.html')

def other_list(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    otheri = OtherIncome.objects.filter(user_id=uid)
    return render(request, 'user/otherlist.html', {'otheri': otheri})

def updateother(request):
    id = request.GET.get('id')
    other = OtherIncome.objects.filter(id=id).first()

    if request.method == "POST":
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']
        frequency = request.POST['frequency']

        other.source = source
        other.amount = amount
        other.date = date
        other.frequency = frequency
        other.save()

        messages.info(request, "Updated Successfully")
        return redirect('/other_list')

    return render(request, "user/otherincome.html", {'other': other})


def deleteother(request):
    id = request.GET.get('id')
    delete = OtherIncome.objects.filter(id=id).delete()
    messages.info(request,"sucessfully Deleted")
    return redirect('/other_list')

##############   FIXED EXPNESIVE      ################

def fixedexpense(request):
    uid = request.session['uid']
    if request.POST:
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']
        # year = request.POST['year']
        frequency = request.POST['frequency']
        
        expense = FixedExpense.objects.create(
            user_id=uid,
            source=source,
            amount=amount,
            # year=year,
            date=date,
            frequency=frequency
        )
        messages.info(request,"successfully Added")
        expense.save()
        return redirect('/expenselist')
    
    return render(request, 'user/fixedexpense.html')


def expenselist(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    exp = FixedExpense.objects.filter(user_id=uid)
    return render(request, 'user/expenselist.html', {'exp': exp})

def updateexpense(request):
    id = request.GET.get('id')
    fixexp = FixedExpense.objects.filter(id=id).first()
    
    if not fixexp:
        messages.error(request, "Expense not found")
        return redirect('/other_list')

    if request.method == "POST":
        fixexp.source = request.POST['source']
        fixexp.date = request.POST['date']
        # fixexp.year = request.POST['year']
        fixexp.amount = request.POST['amount']
        fixexp.frequency = request.POST['frequency']
        fixexp.save()

        messages.success(request, "Updated Successfully")
        return redirect('/expenselist')

    return render(request, "user/fixedexpense.html", {'fixexp': fixexp})


def deleteexpense(request):
    id = request.GET.get('id')
    delete = FixedExpense.objects.filter(id=id).delete()
    messages.info(request,"sucessfully Deleted")
    return redirect('/expenselist')

##############      OTHER EXPENSE     ####################


def otherexpense(request):
    uid = request.session['uid']
    if request.POST:
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']
        frequency = request.POST['frequency']
        
        otrexp = OtherExpense.objects.create(
            user_id=uid,
            source=source,
            amount=amount,
            date=date,
            frequency=frequency
        )
        messages.info(request,"successfully Added")
        otrexp.save()
        return redirect('/otherexplist')
    
    return render(request, 'user/otherexpense.html')

def otherexplist(request):
    id = request.GET.get("id")
    uid = request.session['uid']
    other = OtherExpense.objects.filter(user_id=uid) 
    return render(request, 'user/otherexplist.html', {'other': other})

def updaexp(request):
    id = request.GET.get('id')
    other = OtherExpense.objects.filter(id=id).first()
    if request.method == "POST":
        source = request.POST['source']
        amount = request.POST['amount']
        date = request.POST['date']
        frequency = request.POST['frequency']

        other.source = source
        other.amount = amount
        other.date = date
        other.frequency = frequency
        other.save()

        messages.info(request, "Updated Successfully")
        return redirect('/otherexplist')
    
    return render(request, "user/otherexpense.html", {'other': other})


def delexpense(request):
    id = request.GET.get('id')
    OtherExpense.objects.filter(id=id).delete()  # Corrected model name
    messages.info(request, "Successfully Deleted")
    return redirect('/otherexplist')

from django.db.models import Sum

def alllist(request):
    query = request.GET.get('search', '').strip()
    if 'uid' not in request.session:
        messages.warning(request, 'You need to log in first.')
        return redirect('/login')
    
    uid = request.session['uid']

    infixed = FixedIncome.objects.filter(user_id=uid)
    otheri = OtherIncome.objects.filter(user_id=uid)
    exp = FixedExpense.objects.filter(user_id=uid)
    other = OtherExpense.objects.filter(user_id=uid)

    total_fixed_income = infixed.aggregate(total=Sum('amount'))['total'] or 0
    total_other_income = otheri.aggregate(total=Sum('amount'))['total'] or 0
    total_monthly_income = total_fixed_income + total_other_income

    total_fixed_expense = exp.aggregate(total=Sum('amount'))['total'] or 0
    total_other_expense = other.aggregate(total=Sum('amount'))['total'] or 0
    total_monthly_expenses = total_fixed_expense + total_other_expense

    net_monthly_income = total_monthly_income - total_monthly_expenses

    # **Annual Calculations**
    total_annual_income = total_monthly_income * 12
    total_annual_expenses = total_monthly_expenses * 12
    net_annual_income = total_annual_income - total_annual_expenses

    # **Net Annual Income Before Deducting Expenses**
    net_annual_income_before_expense = total_annual_income  # Income without expenses

    # **Tax Calculation** (7% if income > 12 Lakhs)
    tax_amount = (net_annual_income_before_expense * 7 / 100) if net_annual_income_before_expense > 1200000 else 0
    net_annual_income_after_tax = net_annual_income_before_expense - tax_amount

    context = {
        'query': query,
        'infixed': infixed,
        'otheri': otheri,
        'exp': exp,
        'other': other,
        'total_monthly_income': total_monthly_income,
        'total_monthly_expenses': total_monthly_expenses,
        'net_monthly_income': net_monthly_income,
        'total_annual_income': total_annual_income,
        'total_annual_expenses': total_annual_expenses,
        'net_annual_income': net_annual_income,
        'net_annual_income_before_expense': net_annual_income_before_expense,
        'tax_amount': tax_amount,
        'net_annual_income_after_tax': net_annual_income_after_tax,
    }

    return render(request, "user/alllist.html", context)


##################################################################################################
                                    #GRAPH
##################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from django.shortcuts import render, redirect
from django.contrib import messages
import matplotlib
matplotlib.use('Agg')
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import defaultdict
from io import BytesIO
import base64
import cv2

def graph(request):
    query = request.GET.get('search', '').strip()
    
    # Check if user is logged in
    if 'uid' not in request.session:
        messages.warning(request, 'You need to log in first.')
        return redirect('/login')
    
    uid = request.session['uid']

    fixed_income_monthly = FixedIncome.objects.filter(user_id=uid).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    other_income_monthly = OtherIncome.objects.filter(user_id=uid).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    fixed_expense_monthly = FixedExpense.objects.filter(user_id=uid).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    other_expense_monthly = OtherExpense.objects.filter(user_id=uid).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')

    # Prepare monthly income and expense data for plotting
    monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0})
    
    # Aggregating income and expense data
    for entry in fixed_income_monthly:
        monthly_data[entry['month']]['income'] += entry['total']
    for entry in other_income_monthly:
        monthly_data[entry['month']]['income'] += entry['total']
    for entry in fixed_expense_monthly:
        monthly_data[entry['month']]['expense'] += entry['total']
    for entry in other_expense_monthly:
        monthly_data[entry['month']]['expense'] += entry['total']

    # Extract sorted lists of months, incomes, and expenses for plotting
    months = sorted(monthly_data.keys())
    monthly_income = [monthly_data[month]['income'] for month in months]
    monthly_expense = [monthly_data[month]['expense'] for month in months]
    month_labels = [month.strftime('%B %Y') for month in months]  # Format months for display

    # Create a line plot for income and expenses
    plt.figure(figsize=(10, 5))
    plt.plot(month_labels, monthly_income, label='Monthly Income', color='green', marker='o')
    plt.plot(month_labels, monthly_expense, label='Monthly Expenses', color='red', marker='o')
    plt.title('Income and Expenses Over Time')
    plt.xlabel('Months')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    graph_url = base64.b64encode(image_png).decode('utf-8')

    # Prepare context for rendering the template
    context = {
        'query': query,
        'total_monthly_income': sum(monthly_income),
        'total_monthly_expenses': sum(monthly_expense),
        'net_monthly_income': sum(monthly_income) - sum(monthly_expense),
        'graph_url': graph_url,
    }

    return render(request, "user/graph.html", context)

def generate_visualization_page(dataset_path):
    try:
        df = pd.read_csv(dataset_path)

        sentiment_mapping = {2: 'Positive', 1: 'Neutral', 0: 'Negative'}
        df['Sentiment_Label'] = df['Sentiment'].map(sentiment_mapping)
        sentiment_counts = df['Sentiment_Label'].value_counts()

        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#152335')
        ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, textprops={'color':'#FCDC7E'})
        plt.savefig('sentiment_pie_chart.png', transparent=True)
        plt.close()

        # Generate a word cloud
        plt.figure(figsize=(8, 6))
        text = ' '.join(df['Description'])
        wordcloud = WordCloud(width=1600, height=1200, background_color='#152335').generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('wordcloud.png', transparent=True)
        plt.close()

    except Exception as e:
        raise RuntimeError(f"Error generating visualizations: {str(e)}")

def generate_visualisation(review):
    plt.figure(figsize=(8, 6))
    wordcloud = WordCloud(width=1600, height=1200, background_color='#152335').generate(review)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('wordcloud.png', transparent=True)
    plt.close()

def billreceipt(request):
    uid = request.session['uid']
    if request.POST:
        source = request.POST['source']
        bill_receipt = request.FILES.get('bill_receipt')
        frequency = request.POST['frequency']

        recipt = Uploadbill.objects.create(
            user_id=uid,
            source=source,
            bill_receipt=bill_receipt,
            frequency=frequency
        )
        messages.info(request,"successfully Added")
        recipt.save()
        return redirect('/userhome')
    
    return render(request, 'user/bill.html')



import os
import cv2
import pytesseract
import re
from django.conf import settings

# Path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update if needed

def preprocess_image(image_name):
    # Construct the full path to the uploaded image
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)

    # Check if the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Error: Image file '{image_path}' does not exist.")

    # Load the image
    img = cv2.imread(image_path)

    # Check if the image was loaded successfully
    if img is None:
        raise ValueError(f"Error: Unable to load image from '{image_path}'. Please check the file format and permissions.")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding for better text clarity
    processed_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    return processed_img

def extract_text(image_name):
    # Preprocess the image and perform OCR
    processed_img = preprocess_image(image_name)
    custom_config = r'--oem 3 --psm 6'  # Example config, adjust as necessary
    text = pytesseract.image_to_string(processed_img, config=custom_config)
    
    # Debug: Print the extracted text
    print("Extracted Text:")
    print(text)

    return text

def parse_bill(text):
    data = {'items': []}  # Initialize with empty items list

    # Flexible patterns to match common fields
    # Invoice Number
    invoice_number_match = re.search(r'(Invoice|Invoice No|Invoice #|Bill No|Bill ID)\s*[:\-]?\s*(\d+)', text, re.IGNORECASE)
    if invoice_number_match:
        data['invoice_number'] = invoice_number_match.group(2)

    # Date
    date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2} [A-Za-z]+ \d{4}|\d{4}[/-]\d{1,2}[/-]\d{1,2})', text)
    if date_match:
        data['date'] = date_match.group(0)

    # Billed To
    billed_to_match = re.search(r'(Billed To|To|Customer|Recipient)\s*:\s*(.+?)(?=\n\n|\n\s*\+?\d{1,3}[-\.\s]?\d{3}[-\.\s]?\d{4})', text, re.DOTALL)
    if billed_to_match:
        data['billed_to'] = billed_to_match.group(2).strip()

    # Items
    item_pattern = re.compile(r'(\w[\w\s]*\w)\s+(\d+)\s+\$?(\d+\.?\d{0,2})\s+\$?(\d+\.?\d{0,2})', re.MULTILINE)
    for match in item_pattern.finditer(text):
        item = {
            'description': match.group(1).strip(),
            'quantity': int(match.group(2)),
            'unit_price': float(match.group(3)),
            'total_price': float(match.group(4))
        }
        data['items'].append(item)

    # Subtotal
    subtotal_match = re.search(r'(Subtotal|Sub Total|Sub-Total)\s*[:\-]?\s*\$?(\d+\.?\d{0,2})', text, re.IGNORECASE)
    if subtotal_match:
        data['subtotal'] = float(subtotal_match.group(2))

    # Total Amount
    total_match = re.search(r'(Total|Grand Total|Amount Due|Amount)\s*[:\-]?\s*\$?(\d+\.?\d{0,2})', text, re.IGNORECASE)
    if total_match:
        data['total'] = float(total_match.group(2))

    return data

# Example Django view function
# def process_invoice(request):
#     image_name = 't4.jpg'

#     try:
#         # Perform OCR and parse the bill data
#         text = extract_text(image_name)
#         parsed_data = parse_bill(text)

#         # Display parsed data (you can render this in a template)
#         print("\nParsed Invoice Data:")
#         for key, value in parsed_data.items():
#             print(f"{key.capitalize()}: {value}")

#         # Optionally render to a template
#         return render(request, 'user/bill.html', {'parsed_data': parsed_data})

#     except Exception as e:
#         print(e,'####')
#         # Handle errors appropriately (maybe render an error template)


def process_invoice(request):
    if request.method == 'POST':
        bill_receipt = request.FILES.get('bill_receipt')

        if bill_receipt:
            print("####################if first")
            # Save the uploaded file to MEDIA_ROOT
            file_path = os.path.join(settings.MEDIA_ROOT, bill_receipt.name)
            with open(file_path, 'wb+') as destination:
                for chunk in bill_receipt.chunks():
                    destination.write(chunk)

            try:
                print("#################### try")

                # Only perform OCR and parse the bill data if the file is uploaded
                print(f"Processing file: {bill_receipt.name}")  # Debug: Print the file name

                text = extract_text(file_path)  # This should work with the full file path
                parsed_data = parse_bill(text)

                # Debug: Print parsed data
                print("\nParsed Invoice Data:")
                for key, value in parsed_data.items():
                    print(f"{key.capitalize()}: {value}")

                # Ensure total amount is displayed for debugging
                if 'total' in parsed_data:
                    print(f"Total Amount Extracted: {parsed_data['total']}")

                # Render to a template with parsed data
                return render(request, 'user/bill.html', {'parsed_data': parsed_data})

            except Exception as e:
                print(f"Error occurred: {str(e)} ########################3")  # This will print the specific error
                messages.error(request, "An error occurred while processing the invoice. Please try again.")
                return redirect('/userhome')  # Redirect to a safe page
        else:
            messages.error(request, "No bill receipt uploaded.")
            return redirect('/userhome')  # Redirect to a safe page

    # If the request is GET, render the bill.html page
    return render(request, 'user/bill.html')

def calculator_view(request):
    return render(request, 'user/cal.html')
def predictprices(request):
    # c.execute("select * from Company")
    # datas=c.fetchall()
    prices = ""
    start = ""
    ends = ""
    data = ""
    if request.POST:

        data = request.POST.get("stock")

        date = request.POST.get("t1")
        # if gethistoricaldata(data):
        # msg="No data found"
        gethistoricaldata(data)

        res = stockprediction()
        print("##########################################################################################")
        print(res)
        prices = res["value"]
        print(prices)
        start = res["result"][0]
        ends = res["result"][1]
        print(start)
        print(ends)

        # dates=["10","11","12"]
        # result=predictprice(dates,prices,29)
        # print(result)
        print(
            "****************************************************************************")

    return render(request, "user/predictprice.html", {"price": prices, "start": start, "ends": ends, "data": data})


ConsumerKey = "zS2ibMBtTpsDu8ekzIKJva8Mj"
ConsumerSecret = "EvsXL1zBLwFo78lHqRXI8Fv3N33uQq0w8620zyCxrE8WesFjVT"
AccessToken = "3041974901-ZRJqJQOUFzt4yiS3KGtd3CBnAocxh1NlUSNIC0x"
AccessTokenSecret = "zOOYb6u9OrWqz2mczVwOPnKAPvDfFappb2lR0VrrbzB1W"
auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
# con=tweepy.API(auth)
# tweets=con.search("oru_adaar_love")
# app=Flask("__name__")


filename = "sto.csv"

dates = []
prices = []


def gethistoricaldata(histo):
    # url='https://finance.google.com/finance/historical?q= %3A'+histo+'&output=csv'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + \
        histo+'&apikey=OXEWYUN5KP4117WN&datatype=csv'
    print(url)
    r = requests.get(url, stream=True)
    if r.status_code != 400:
        with open(filename, "wb") as f:
            for line in r:
                f.write(line)

        return True

        # print(getNews(x))


def stockprediction():
    dataset = []
    with open(filename) as f:
        for n, line in enumerate(f):
            if n != 0:
                dataset.append(float(line.split(',')[1]))
        dataset = np.array(dataset)

        def createdataset(dataset):
            datax = [dataset[n+1] for n in range(len(dataset)-2)]
            return np.array(datax), dataset[2:]
        trainx, trainy = createdataset(dataset)
        model = Sequential()  # Process 1st layer then 2nd
        # ann model 8 layers, input_diamention 1(one diamentional array)
        model.add(Dense(8, input_dim=1, activation='relu'))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(trainx, trainy, epochs=20, batch_size=2, verbose=2)
        prediction = model.predict(np.array([dataset[0]]))
        result = [dataset[0], prediction[0, 0]]
        print(result)
        dictionary = {"value": str(prediction[0, 0]), "result": result}
        return (dictionary)


def getdata(filename):
    with open(filename, 'r') as csvfile:
        csvfilereader = csv.reader(csvfile)
        next(csvfilereader)
        for raw in csvfilereader:
            dates.append(int(raw[0].split('-')[0]))
            prices.append(float(raw[1]))
    return


def predictprice(dates, prices, x):
    dates = np.reshape(dates, (len(dates), 1))
    svrline = SVR(kernel='linear', C=1e3)
    svrpoly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rpf = SVR(kernel='rbf', C=1e3, gamma=.1)
    svrline.fit(dates, prices)
    svrpoly.fit(dates, prices)
    svr_rpf.fit(dates, prices)
    plot.scatter(dates, prices, color='black', label='DATA')
    plot.plot(dates, svr_rpf.predict(dates), color='red', label='rbf_model')
    plot.plot(dates, svrline.predict(dates), color='blue', label='line_model')
    plot.plot(dates, svrpoly.predict(dates), color='green', label='ploy_model')
    plot.xlabel('DATE')
    plot.ylabel('price')
    plot.title("Stock Prediction")
    plot.legend()
    plot.show()
    return svr_rpf.predict(x)[0], svrline.predict(x)[0], svrpoly.predict(x)[0]
