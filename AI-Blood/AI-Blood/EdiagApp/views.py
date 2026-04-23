from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db.models import Q
from datetime import date, datetime

import numpy as np
import pandas as pd

from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 

from django.core.files import File
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent



# Create your views here.

def Index(request):
    return render(request,'index.html')

def login(request):
    if request.POST:
        usname = request.POST["username"]
        pasw = request.POST["password"]
        check_cust_user = authenticate(username=usname,password = pasw)
        if check_cust_user is not None:
                if check_cust_user.is_superuser == True:
                    messages.info(request,"Login successfull")
                    return redirect("/admin_home")
                elif check_cust_user.is_staff == True:
                    chef = LabReg.objects.get(email = usname)
                    request.session['uid'] = chef.id
                    messages.info(request,"Login successfull")
                    return redirect("/lab_home")
                elif check_cust_user.is_staff == False:
                    du = UserReg.objects.get(email = usname)
                    request.session['uid'] = du.id
                    messages.info(request,"Login successfull")
                    return redirect("/user_home")
        elif User.objects.filter(username = usname):
            cust = User.objects.get(username = usname)
            if cust.is_active == 0:
                messages.info(request,"User not approved")
            else:
                messages.info(request,"Password not matching")
        else:
            messages.info(request,"User dosent exist")
    return render(request,'login.html')

def client_reg(request):
    if request.POST:
        first_name = request.POST["fname"]
        last_name = request.POST["lname"]
        contact =  request.POST["phone"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        address = request.POST["address"]
        if UserReg.objects.filter(Q(user__username = username) | Q(contact = contact)).exists():
            messages.info(request,"Email or phone no is taken")
        else:
            dataToUser = User.objects.create_user(first_name = first_name,
                                            last_name = last_name,
                                            username = username,
                                            email = email,
                                            password = password,
                                            is_staff = 0,
                                            is_active = 1)
            dataToUser.save()
            dataToReg = UserReg.objects.create(first_name = first_name,
                                                last_name = last_name,
                                                contact = contact,
                                                email = username,
                                                address = address,
                                                user = dataToUser,
                                                pwd=password)
            dataToReg.save()
            messages.info(request,"User Registered")
            return redirect("/login")
    return render(request,'client_reg.html')

def lab_reg(request):
    if request.POST:
        first_name = request.POST["fname"]
        location = request.POST["loc"]
        contact =  request.POST["phone"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        address = request.POST["address"]
        if LabReg.objects.filter(Q(user__username = username) | Q(contact = contact)).exists():
            messages.info(request,"Email or phone no is taken")
        else:
            dataToUser = User.objects.create_user(first_name = first_name,
                                            username = username,
                                            email = email,
                                            password = password,
                                            is_staff = 1,
                                            is_active = 0)
            dataToUser.save()
            dataToReg = LabReg.objects.create(name = first_name,
                                                location = location,
                                                contact = contact,
                                                email = username,
                                                address = address,
                                                user = dataToUser,
                                                pwd=password)
            dataToReg.save()
            messages.info(request,"Lab Registered")
            return redirect("/login")
    return render(request,'lab_reg.html')

def admin_home(request):
    # diseasedetected = None
    # # global cosfound
    # cosfound = None
    # if request.POST:
    #     WBC = request.POST["WBC"]
    #     RBC = request.POST["RBC"]
    #     HGB = request.POST["HGB"]
    #     PLT = request.POST["PLT"]
    #     NEUT = request.POST["NEUT"]
    #     LYMPH = request.POST["LYMPH"]
    #     MONO = request.POST["MONO"]
    #     EO = request.POST["EO"]
    #     BASO = request.POST["BASO"]
    #     # Diseases

    #     disease = { 0:'Anemia',
    #     1:'Polycythemia',
    #     2:'Leukocytosis',
    #     3:'Leukopenia',
    #     4:'Thrombocytopenia',
    #     5:'Thrombocytosis',
    #     6:'Neutropenia',
    #     7:'Neutrophilia',
    #     8:'Lymphocytopenia',
    #     9:'Lymphocytosis',
    #     10:'Monocytes high',
    #     11:'Eosinophil high',
    #     12:'Basophil high',
    #     13:'Normal'}


    #     # Causes

    #     Rea = { 0:[' - Anemia due to blood loss \n'
    #     ' - Bone marrow disorders \n'
    #     ' - Nutritional deficiency \n'
    #     ' - Chronic Kidney disease  \n'
    #     ' - Chronic inflammatory disease \n'],
    #     1:['- Dehydration, such as from severe diarrhea \n'
    #     '- tumours \n'
    #     '- Lung diseases \n'
    #     '- Smoking \n'
    #     '- Polycythemia vera \n'],
    #     2:['- Infection \n'
    #     '- Leukemia \n'
    #     '- Inflammation \n'
    #     '- Stress, allergies, asthma \n'],
    #     3:['- Viral infection \n'
    #     '- Severe bacterial infection \n'
    #     '- Bone marrow disorders \n'
    #     '- Autoimmune conditions \n'
    #     '- Lymphoma \n'
    #     '- Dietary deficiencies \n'],
    #     4:['- Cancer, such as leukemia or lymphoma \n'
    #     '- Autoimmune diseases \n'
    #     '- Bacterial infection \n'
    #     '- Viral infection like dengue \n'
    #     '- Chemotherapy or radiation therapy \n'
    #     '- Certain drugs, such as nonsteroidal anti-inflammatory drugs (NSAIDs) \n' ],
    #     5:['- Bone marrow disorders \n'
    #     '- Essential thrombocythemia \n'
    #     '- Anemia \n'
    #     '- Infection \n'
    #     '- Surgical removal of the spleen \n'
    #     '- Polycythemia vera \n'
    #     '- Some types of leukemia \n'],
    #     6:['- Severe infection \n'
    #     '- Immunodeficiency \n'
    #     '- Autoimmune disorders \n'
    #     '- Dietary deficiencies \n'
    #     '- Reaction to drugs \n'
    #     '- Bone marrow damage \n'],
    #     7:['- Acute bacterial infections \n'
    #     '- Inflammation \n'
    #     '- Stress, Trauma \n'
    #     '- Certain leukemias \n'],
    #     8:['- Autoimmune disorders \n'
    #     '- Infections \n'
    #     '- Bone marrow damage \n'
    #     '- Corticosteroids \n'],
    #     9:['- Acute viral infections \n'
    #     '- Certain bacterial infections \n'
    #     '- Chronic inflammatory disorder \n'
    #     '- Lymphocytic leukemia, lymphoma \n'
    #     '- Acute stress \n'],
    #     10:['- Chronic infections \n'
    #     '- Infection within the heart \n'
    #     '- Collagen vascular diseases \n'
    #     '- Monocytic or myelomonocytic leukemia \n'],
    #     11:['- Asthma, allergies such as hay fever \n'
    #     '- Drug reactions \n'
    #     '- Parasitic infections \n'
    #     '- Inflammatory disorders \n'
    #     '- Some cancers, leukemias or lymphomas \n'],
    #     12:['- Rare allergic reactions \n'
    #     '- Inflammation \n'
    #     '- Some leukemias \n'
    #     '- Uremia \n'],
    #     13:['- Normal \n']}


    #     # Random Forest Algorothm

    #     def rf(W,R,H,P,N,L,M,E,B):
    #         from sklearn.ensemble import RandomForestClassifier
    #         from sklearn.model_selection import train_test_split
    #         data= pd.read_csv("C:/Users/lenovo/Desktop/ABI/2024/BLOOD/Ediagnostic/EdiagApp/Training.csv")
    #         x=data.drop(columns=['Disease'],axis=1)
    #         y=data['Disease']
    #         x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=40) 
    #         clf = RandomForestClassifier(n_estimators = 100)
    #         clf.fit(x_train, y_train)
    #         t = np.array([W,R,H,P,N,L,M,E,B])
    #         t=t.reshape(1,-1)
    #         res=clf.predict(t)[0]
    #         for i in disease:
    #             if(i==res):
    #                 nonlocal cosfound
    #                 cosfound = Rea[i][0]
    #                 return(disease[i])


    #     diseasedetected = rf(WBC,RBC,HGB,PLT,NEUT,LYMPH,MONO,EO,BASO)
    # return render(request,'admin_home.html',{"diseasedetected":diseasedetected,"causes":cosfound})
    return render(request,'admin_home.html')

def admin_client(request):
    data = UserReg.objects.all()
    return render(request,'admin_client.html',{"data":data})

def admin_lab(request):
    data = LabReg.objects.all()
    return render(request,'admin_lab.html',{"data":data})

def admin_action(request):
    id = request.GET.get("id")
    action = request.GET.get("action")
    if(action == "clientBlock"):
        client = UserReg.objects.get(id = id)
        client.user.is_active = 0
        client.user.save()
        return redirect("/admin_client")
    elif(action == "clientApprove"):
        client = UserReg.objects.get(id = id)
        client.user.is_active = 1
        client.user.save()
        return redirect("/admin_client")
    elif(action == "labBlock"):
        client = LabReg.objects.get(id = id)
        client.user.is_active = 0
        client.user.save()
        return redirect("/admin_lab")
    elif(action == "labApprove"):
        client = LabReg.objects.get(id = id)
        client.user.is_active = 1
        client.user.save()
        return redirect("/admin_lab")
    elif(action == "testDel"):
        client = Tests.objects.get(id = id)
        client.delete()
        return redirect("/admin_tests")

def admin_tests(request):
    data = Tests.objects.all()
    return render(request,'admin_tests.html',{"data":data})

def admin_orders(request):
    data = Slots.objects.all().order_by("-id")
    return render(request,'admin_orders.html',{"data":data})

def admin_payments(request):
    data = Payment.objects.all()
    return render(request,'admin_payments.html',{"data":data})


def lab_home(request):
    return render(request,'lab_home.html')

def lab_tests(request):
    userid = request.session["uid"]
    lab = LabReg.objects.get(id = userid)
    data = Tests.objects.filter(lab__id = userid)
    if request.POST:
        test = request.POST["test"]
        description = request.POST["description"]
        price = request.POST["price"]
        if Tests.objects.filter(Q(lab__id = userid) & Q(test = test)).exists():
            messages.info(request,"This test alredy eexists")
        else:
            toTest = Tests.objects.create(lab = lab,
                                        test = test,
                                        description = description,
                                        price = price)
            toTest.save()
    return render(request,'lab_tests.html',{"data":data})

def labDelTest(request):
    id = request.GET.get("id")
    Task = Tests.objects.get(id = id)
    Task.delete()
    return redirect("/lab_tests")

def lab_slots(request):
    userid = request.session["uid"]
    lab = LabReg.objects.get(id = userid)
    if request.POST:
        date = request.POST["date"]
        time = request.POST["time"]
        if Slots.objects.filter(Q(lab__id = userid) & Q(date = date) & Q(time = time)).exists():
            messages.info(request,"This slot alredy eexists")
        else:
            toTest = Slots.objects.create(lab = lab,
                                        date = date,
                                        time = time)
            toTest.save()
    data = Slots.objects.filter(lab__id=userid)
    return render(request,'lab_slots.html',{"data":data})

def lab_completed(request):
    id = request.GET.get("id")
    Task = Slots.objects.get(id = id)
    Task.testStatus = 1
    Task.save()
    return redirect("/lab_slots")

def lab_addReport(request):
    id = request.GET.get("id")
    Task = Slots.objects.get(id = id)
    if request.POST:
        report = request.FILES["report"]
        Task.report = report
        Task.save()
    return render(request,"lab_addReport.html",{"Task":Task})

def lab_add_blood_report(request):
    diseasedetected = None
    # global cosfound
    cosfound = None
    if request.POST:
        sid = request.POST["sid"]
        Task = Slots.objects.get(id = sid)
        WBC = request.POST["WBC"]
        RBC = request.POST["RBC"]
        HGB = request.POST["HGB"]
        PLT = request.POST["PLT"]
        NEUT = request.POST["NEUT"]
        LYMPH = request.POST["LYMPH"]
        MONO = request.POST["MONO"]
        EO = request.POST["EO"]
        BASO = request.POST["BASO"]
        # Diseases

        disease = { 0:'Anemia',
        1:'Polycythemia',
        2:'Leukocytosis',
        3:'Leukopenia',
        4:'Thrombocytopenia',
        5:'Thrombocytosis',
        6:'Neutropenia',
        7:'Neutrophilia',
        8:'Lymphocytopenia',
        9:'Lymphocytosis',
        10:'Monocytes high',
        11:'Eosinophil high',
        12:'Basophil high',
        13:'Normal'}


        # Causes

        Rea = { 0:[' - Anemia due to blood loss \n',
        ' - Bone marrow disorders \n',
        ' - Nutritional deficiency \n',
        ' - Chronic Kidney disease  \n',
        ' - Chronic inflammatory disease \n'],
        1:['- Dehydration, such as from severe diarrhea \n',
        '- tumours \n',
        '- Lung diseases \n',
        '- Smoking \n',
        '- Polycythemia vera \n'],
        2:['- Infection \n',
        '- Leukemia \n',
        '- Inflammation \n',
        '- Stress, allergies, asthma \n'],
        3:['- Viral infection \n',
        '- Severe bacterial infection \n',
        '- Bone marrow disorders \n',
        '- Autoimmune conditions \n',
        '- Lymphoma \n',
        '- Dietary deficiencies \n'],
        4:['- Cancer, such as leukemia or lymphoma \n',
        '- Autoimmune diseases \n',
        '- Bacterial infection \n',
        '- Viral infection like dengue \n',
        '- Chemotherapy or radiation therapy \n',
        '- Certain drugs, such as NSAIDs \n' ],
        5:['- Bone marrow disorders \n',
        '- Essential thrombocythemia \n',
        '- Anemia \n',
        '- Infection \n',
        '- Surgical removal of the spleen \n',
        '- Polycythemia vera \n',
        '- Some types of leukemia \n'],
        6:['- Severe infection \n',
        '- Immunodeficiency \n',
        '- Autoimmune disorders \n',
        '- Dietary deficiencies \n',
        '- Reaction to drugs \n',
        '- Bone marrow damage \n'],
        7:['- Acute bacterial infections \n',
        '- Inflammation \n',
        '- Stress, Trauma \n',
        '- Certain leukemias \n'],
        8:['- Autoimmune disorders \n',
        '- Infections \n',
        '- Bone marrow damage \n',
        '- Corticosteroids \n'],
        9:['- Acute viral infections \n',
        '- Certain bacterial infections \n',
        '- Chronic inflammatory disorder \n',
        '- Lymphocytic leukemia, lymphoma \n',
        '- Acute stress \n'],
        10:['- Chronic infections \n',
        '- Infection within the heart \n',
        '- Collagen vascular diseases \n',
        '- Monocytic or myelomonocytic leukemia \n'],
        11:['- Asthma, allergies such as hay fever \n',
        '- Drug reactions \n',
        '- Parasitic infections \n',
        '- Inflammatory disorders \n',
        '- Some cancers, leukemias or lymphomas \n'],
        12:['- Rare allergic reactions \n',
        '- Inflammation \n',
        '- Some leukemias \n',
        '- Uremia \n'],
        13:['- Normal \n']}


        # Random Forest Algorothm

        def rf(W,R,H,P,N,L,M,E,B):
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split
            # data= pd.read_csv("C:/Users/lenovo/Desktop/ABI/2024/BLOOD/Ediagnostic/EdiagApp/Training.csv")
            data= pd.read_csv(BASE_DIR / "EdiagApp/Training.csv")
            x=data.drop(columns=['Disease'],axis=1)
            y=data['Disease']
            x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=40) 
            clf = RandomForestClassifier(n_estimators = 100)
            clf.fit(x_train, y_train)
            t = np.array([W,R,H,P,N,L,M,E,B])
            t=t.reshape(1,-1)
            res=clf.predict(t)[0]
            for i in disease:
                if(i==res):
                    nonlocal cosfound
                    cosfound = Rea[i][0:]
                    return(disease[i])
        diseasedetected = rf(WBC,RBC,HGB,PLT,NEUT,LYMPH,MONO,EO,BASO)
        print(diseasedetected,"DDDDDDDDDDDDDDD")
        print(cosfound,'cccccccccccccccccccc')

        # initializing variables with values 
        fileName = 'sample.pdf'
        documentTitle = 'Blood Test Report'
        title = 'Blood Test Report'
        subTitle = str(datetime.now().strftime("generated on %Y-%m-%d at %H:%M:%S"))

        # | *Parameter* | *Minimum* | *Maximum* |
        # |---------------|-------------|-------------|
        # | *WBC*       | 1.3         | 33.0        |
        # | *RBC*       | 3.0         | 7.77        |
        # | *HGB*       | 4.6         | 18.4        |
        # | *PLT*       | 21          | 654         |
        # | *NEUT*      | 1.2         | 9.0         |
        # | *LYMPH*     | 0.5         | 6.7         |
        # | *MONO*      | 0.07        | 3.3         |
        # | *EOS*       | 0.03        | 5.05        |
        # | *BASO*      | 0.01        | 0.43        |

        exceededValues = ['Readings:']
        leastValues = []
        normalValues = []
        if int(WBC) < 1.3 :
            leastValues.append("WBC :"+WBC)
        elif int(WBC) > 33.0:
            exceededValues.append("WBC :"+WBC)
        else:
            normalValues.append("WBC :"+WBC)

        if int(RBC) < 3.0:
            leastValues.append("RBC :"+RBC)
        elif int(RBC) > 7.77:
            exceededValues.append("RBC :"+RBC)
        else:
            normalValues.append("RBC :"+RBC)

        if int(HGB) < 4.6:
            leastValues.append("HGB :"+HGB)
        elif int(HGB) > 18.4:
            exceededValues.append("HGB :"+HGB)
        else:
            normalValues.append("HGB :"+HGB)

        if int(PLT) < 21:
            leastValues.append("PLT :"+PLT)
        elif int(PLT) > 654:
            exceededValues.append("PLT :"+PLT)
        else:
            normalValues.append("PLT :"+PLT)

        if int(NEUT) < 1.2:
            leastValues.append("NEUT :"+NEUT)
        elif int(NEUT) > 9.0:
            exceededValues.append("NEUT :"+NEUT)
        else:
            normalValues.append("NEUT :"+NEUT)

        if int(LYMPH) < 0.5:
            leastValues.append("LYMPH :"+LYMPH)
        elif int(LYMPH) > 6.7:
            exceededValues.append("LYMPH :"+LYMPH)
        else:
            normalValues.append("LYMPH :"+LYMPH)

        if int(MONO) < 0.07:
            leastValues.append("MONO :"+MONO)
        elif int(MONO) > 3.3:
            exceededValues.append("MONO :"+MONO)
        else:
            normalValues.append("MONO :"+MONO)

        if int(EO) < 0.03:
            leastValues.append("EO :"+EO)
        elif int(EO) > 5.05:
            exceededValues.append("EO :"+EO)
        else:
            normalValues.append("EO :"+EO)

        if int(BASO) < 0.01:
            leastValues.append("BASO :"+BASO)
        elif int(BASO) > 0.43:
            exceededValues.append("BASO :"+BASO)
        else:
            normalValues.append("BASO :"+BASO)

        print(exceededValues,"Exceeded")
        print(leastValues,"Least")
        print(normalValues,"Normal")


        # valuess = [
        #     'Readings:',
        #     "WBC: "+WBC,
        #     "RBC: "+RBC,
        #     "HGB: "+HGB,
        #     "PLT: "+PLT,
        #     "NEUT: "+NEUT,
        #     "LYMPH: "+LYMPH,
        #     "MONO: "+MONO,
        #     "EO: "+EO,
        #     "BASO: "+BASO
        # ]
        cosfound.insert(0,"Causes :")
        textLines = cosfound
        print(type(textLines))
        print(textLines)
        textLines.insert(0,diseasedetected)
        textLines.insert(0,"Disease detected : ")
        # image = 'image.jpg'
        
        # creating a pdf object 
        pdf = canvas.Canvas(fileName) 

        # setting the title of the document 
        pdf.setTitle(documentTitle)
        
        # # registering a external font in python 
        # pdfmetrics.registerFont( 
        #     TTFont('abc', 'SakBunderan.ttf') 
        # ) 


        # creating the title by setting it's font
        # and putting it on the canvas 
        # pdf.setFont('abc', 36) 
        pdf.drawCentredString(300, 770, title) 
        
        # creating the subtitle by setting it's font,  
        # colour and putting it on the canvas 
        pdf.setFillColorRGB(0, 0, 255) 
        # pdf.setFont("Courier-Bold", 24) 
        pdf.drawCentredString(290, 720, subTitle) 
        
        # drawing a line 
        pdf.line(30, 710, 550, 710) 


        # creating a multiline text using  
        # textline and for loop 
        text = pdf.beginText(40, 680) 
        text.setFont("Courier", 18) 
        text.setFillColor(colors.purple)
        for line in textLines: 
            text.textLine(line)
        text.setFillColor(colors.red)
        for line in exceededValues: 
            text.textLine(line)
        text.setFillColor(colors.green)
        for line in normalValues:
            text.textLine(line)
        text.setFillColor(colors.yellowgreen)
        for line in leastValues:
            text.textLine(line)
        pdf.drawText(text)
        
        # drawing a image at the  
        # specified (x.y) position 
        # pdf.drawInlineImage(image, 130, 400) 
        
        # saving the pdf 
        pdf.save()
        # file_path = "C:/Users/lenovo/Desktop/ABI/2024/BLOOD/Ediagnostic/sample.pdf"
        file_path = BASE_DIR / "sample.pdf"
        with open(file_path, "rb") as f:
            django_file = File(f)
            # Save the file into the FileField
            Task.report.save(Path(file_path).name, django_file)
            Task.save()
    # return redirect("/lab_slots")


def user_home(request):
    return render(request,'user_home.html')

def user_labs(request):
    data = LabReg.objects.all()
    return render(request,'user_labs.html',{"data":data})

def user_slots(request):
    labid = request.GET.get("id")
    if not labid:
        messages.info(request, "Invalid lab")
        return redirect("/user_home")

    lab = LabReg.objects.get(id=labid)
    today = date.today()
    data = Slots.objects.filter(Q(lab__id=labid) & Q(date__gt=today))

    dates = []
    for i in data:
        dates.append(i.date)
    dates = list(set(dates))

    return render(request, 'user_slots.html', {
        "data": data,
        "lab": lab,
        "dates": dates
    })

def user_bookslot(request):
    userid = request.session["uid"]
    user = UserReg.objects.get(id=userid)

    slotid = request.GET.get("id")
    slot = Slots.objects.get(id=slotid)

    data = Tests.objects.filter(lab__id=slot.lab.id)

    if request.POST:
        testid = request.POST.get("test")
        test = Tests.objects.get(id=testid)

        slot.user = user
        slot.test = test
        slot.testStatus = 1   # ✅ MARK AS SUCCESS
        slot.save()

        messages.success(request, "Slot booked successfully")
        return redirect("/user_bookings")  # your bookings page

    return render(request, 'user_bookslot.html', {"data": data})

def user_bookings(request):
    userid = request.session["uid"]
    user = UserReg.objects.get(id = userid)
    slot = Slots.objects.filter(user__id=userid).order_by("-id")
    return render(request,'user_bookings.html',{"data":slot})

def user_tests(request):
    data = Tests.objects.all()
    return render(request,'user_tests.html',{"data":data})

def user_pay(request):
    userid = request.session["uid"]
    user = UserReg.objects.get(id = userid)
    slotid = request.GET.get("sid")
    slot = Slots.objects.get(id = slotid)
    amount = slot.test.price
    if request.POST:
        payment = Payment.objects.create(amount = amount,
                                        user = user,
                                        slot = slot)
        payment.save()
        slot.testStatus = 2
        slot.save()
        return redirect(f"/user_bookings")
    return render(request,'user_pay.html',{"amt":amount})

def user_payments(request):
    userid = request.session["uid"]
    data = Payment.objects.filter(user__id = userid)
    return render(request,'user_payments.html',{"data":data})


# disease_map = {
#     0: "No Disease",
#     1: "Anemia",
#     2: "Leukemia",
#     3: "Iron Deficiency",
#     4: "Thalassemia",
#     5: "Vitamin B12 Deficiency",
#     6: "Infection",
#     7: "Hemophilia",
#     8: "Sickle Cell",
#     9: "Myelodysplastic Syndrome",
#     10: "Polycythemia",
#     11: "Lymphoma",
#     12: "Chronic Disease",
#     13: "Other Blood Disorder"
# }

# def admin_add_test(request):
#     result = None
#     if request.method == "POST":
#         WBC = float(request.POST["WBC"])
#         RBC = float(request.POST["RBC"])
#         HGB = float(request.POST["HGB"])
#         PLT = float(request.POST["PLT"])
#         NEUT = float(request.POST["NEUT"])
#         LYMPH = float(request.POST["LYMPH"])
#         MONO = float(request.POST["MONO"])
#         EOS = float(request.POST["EOS"])
#         BASO = float(request.POST["BASO"])
        
#         # Predict disease
#         test_data = [[WBC,RBC,HGB,PLT,NEUT,LYMPH,MONO,EOS,BASO]]
#         pred_num = model.predict(test_data)[0]
#         pred_name = disease_map.get(pred_num, "Unknown Disease")
        
#         # Save to database
#         result = BloodTest.objects.cre


def select_lab_blood(request):
    labs = LabReg.objects.all()

    if request.method == "POST":
        request.session['lab_id'] = request.POST['lab_id']
        return redirect('/blood_payment')

    return render(request, 'select_lab_blood.html', {'labs': labs})


def blood_payment(request):
    uid = request.session['uid']
    lab_id = request.session['lab_id']

    user = UserReg.objects.get(id=uid)
    lab = LabReg.objects.get(id=lab_id)

    if request.method == "POST":
        BloodTestBooking.objects.create(
            user=user,
            lab=lab,
            payment_status="Paid"
        )
        messages.info(request, "Payment successful")
        return redirect('/user_home')

    return render(request, 'blood_payment.html', {
        'lab': lab
    })

def user_blood_bookings(request):
    uid = request.session['uid']
    user = UserReg.objects.get(id=uid)

    bookings = BloodTestBooking.objects.filter(user=user).order_by('-booking_date')

    return render(request, 'user_blood_bookings.html', {
        'bookings': bookings
    })

    
from .models import BloodTestBooking, LabReg

def view_blood_bookings(request):
    uid = request.session['uid']
    lab = LabReg.objects.get(id=uid)

    bookings = BloodTestBooking.objects.filter(
        lab=lab,
        payment_status="Paid"
    ).order_by('-booking_date')

    return render(request, 'view_blood_bookings.html', {
        'bookings': bookings
    })


import pickle
import numpy as np
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from io import BytesIO
from .ml.disease_map import disease_map
from .models import BloodTestBooking

def upload_blood_report(request, booking_id):
    booking = BloodTestBooking.objects.get(id=booking_id)

    if request.POST:
        WBC = float(request.POST['WBC'])
        RBC = float(request.POST['RBC'])
        HGB = float(request.POST['HGB'])
        PLT = float(request.POST['PLT'])
        NEUT = float(request.POST['NEUT'])
        LYMPH = float(request.POST['LYMPH'])
        MONO = float(request.POST['MONO'])
        EOS = float(request.POST['EOS'])
        BASO = float(request.POST['BASO'])

        with open("Ediagnostic/ml/blood_model.pkl", "rb") as f:
            model = pickle.load(f)

        prediction = model.predict([[WBC,RBC,HGB,PLT,NEUT,LYMPH,MONO,EOS,BASO]])[0]
        disease = disease_map[prediction]

        booking.predicted_disease = disease

        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "Blood Test Diagnostic Report")
        p.drawString(100, 720, f"Patient: {booking.user.first_name}")
        p.drawString(100, 690, f"Predicted Disease: {disease}")
        p.drawString(100, 660, f"WBC: {WBC}, RBC: {RBC}, HGB: {HGB}")
        p.drawString(100, 630, f"PLT: {PLT}, NEUT: {NEUT}")
        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()

        booking.pdf_report.save(
            f"report_{booking.id}.pdf",
            ContentFile(pdf)
        )
        booking.save()

        return redirect('/view_blood_bookings')

    return render(request, "upload_blood_report.html", {"booking": booking})

