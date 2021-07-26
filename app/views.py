from django.core.checks import messages
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import make_password,check_password
import datetime
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from datetime import timedelta
from datetime import date
from datetime import datetime
from datetime import *


from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import pytz
from google.oauth2 import service_account

import os





# Create your views here.
def Singup(request):
    if request.method=="POST":
        username = request.POST['user_name']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        isUsernameexist = User_Master.objects.filter(Username=username)
        isEmailexist = User_Master.objects.filter(Email=email)
        
        print("=================")
        print(role)
        if role == 'Select Role':
            message = "Select Role First"
            data = {
                'username':username,
                'email':email,
                'password':password,
                'cpassword':cpassword,
                'msg':message
            }
            return render(request,"singup.html",data)
        elif isUsernameexist:
            message = "Username Already Exist"
            data = {
                'email':email,
                'password':password,
                'cpassword':cpassword,
                'msg':message
            }
            return render(request,"singup.html",data)

        elif isEmailexist:
            message = "This Email Already Exist"
            data = {
                'username':username,
                'password':password,
                'cpassword':cpassword,
                'msg':message
            }
            return render(request,"singup.html",data)
        elif password!=cpassword:
            message = "Confirm Password Dose Not Match"
            data = {
                'username':username,
                'email':email,
                'msg':message
            }
            return render(request,"singup.html",data)
        else :
            message = "Account Created"
            data = {
                'username':username,
                'role':role,
                'email':email,
                'password':password,
                'cpassword':cpassword,
                'msg':message
            }
            return render(request,"enter_profile_data.html",data)

            


        return render(request,"singup.html")


    else:
        return render(request,"singup.html")

def Submit_data(request):
    if request.method=="POST":
        username = request.POST['user_name']
        email = request.POST['email']
        role = request.POST['role']
        password1 = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        #Password encrypted_
        password=make_password(password1)
        try:
            if request.FILES['profile_pic']:
                profile_pic = request.FILES['profile_pic']        
        except:
            profile_pic = ""

        new_user = User_Master.objects.create(
            Username = username,
            Email = email,
            Password = password,
            Role = role,
        )

        if new_user.Role == 'Doctor':
            new_doctor = Doctor.objects.create(
                User_Master=new_user,
                First_Name = first_name,
                Last_Name = last_name,
                Profile_Picture = profile_pic,
                Address = address,
                City = city,
                State = state,
                Pin_Code = pincode,
            )
             
            request.session['pic']=new_doctor.Profile_Picture.url
            request.session['fname']=new_doctor.First_Name
            request.session['lname']=new_doctor.Last_Name 
            request.session['id'] = new_user.id 
            return redirect('posts')
        elif new_user.Role == 'Patient':
            new_patient = Patient.objects.create(
                User_Master=new_user,
                First_Name = first_name,
                Last_Name = last_name,
                Profile_Picture = profile_pic,
                Address = address,
                City = city,
                State = state,
                Pin_Code = pincode,
            )
            request.session['id'] = new_user.id 
            return redirect('index')


  
   
    
    
def Login(request):
    if request.method=="POST":
        email = request.POST['email']
        password = request.POST['password']
        isEmailexist = User_Master.objects.filter(Email=email)
        if isEmailexist:
            user = User_Master.objects.get(Email=email)
            # if password == user.Password:
            if check_password(password,user.Password):
                request.session['id'] = user.id
                if user.Role == 'Doctor':
                    return redirect('posts')
                else:
                    return redirect('index')
            else:
                message = "Incorect Password!!"
                data ={
                    'msg':message,
                    'email':email,
                    'password':password
                }
                return render(request,"login.html",data)

        else:
            message = "This Email Not Registed With Any Account"
            data ={
                'msg':message,
                'email':email,
                'password':password
            }
            return render(request,"login.html",data)
            
    return render(request,"login.html")

def Dashboard(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    if user.Role == 'Doctor':
        doctor = Doctor.objects.get(User_Master=user)
        request.session['pic']=doctor.Profile_Picture.url
        request.session['fname']=doctor.First_Name
        request.session['lname']=doctor.Last_Name

        print(doctor.Profile_Picture.url)
        data = {
            'user':user,
            'doctor':doctor
        }
        return render(request,"doctor/doctor_profile.html",data)
    else:
        patient = Patient.objects.get(User_Master=user)
        request.session['pic']=patient.Profile_Picture.url
        request.session['fname']=patient.First_Name
        request.session['lname']=patient.Last_Name
        data = {
            'user':user,
            'patient':patient
        }
        return render(request,"patient/patient_profile.html",data)

def Logout(request):
    del request.session['id']
    del request.session['fname']
    del request.session['lname']
    del request.session['pic']
    return redirect('login')


def temp(request):
    return render(request,"temp.html")

def category(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    doctor = Doctor.objects.get(User_Master=user)
    category = Category.objects.filter(Doctor=doctor)
    
    paginator = Paginator(category,2)
    page = request.GET.get('page')
    paged_category = paginator.get_page(page)
   

    data = {
        'category':paged_category
    }
    return render(request,"doctor/category.html",data)

def add_category(request):
    if request.method=="POST":
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        doctor = Doctor.objects.get(User_Master=user)

        category_name = request.POST['category_name']

        isCategoryexist = Category.objects.filter(Category_name=category_name)
        if isCategoryexist:
            message = "Category Already Exist!!"
            data = {
                'msg':message
            }
            return render(request,"doctor/add_category.html",data)
        else:
            new_Category = Category.objects.create(
                Category_name=category_name,
                Doctor=doctor
                )
            message = "Category Added successfully."
            data = {
                'msg':message
            }
            return render(request,"doctor/add_category.html",data)


    return render(request,"doctor/add_category.html")


def update_category(request,key):
  category = Category.objects.get(id=key)
  if request.method=="POST":
        category_name = request.POST['category_name']
        category.Category_name = category_name
        category.save()
        return redirect('category')
  else:
    data = {
        'category':category
    }
    return render(request,"doctor/add_category.html",data)


def delete_category(request,key):
  category = Category.objects.get(id=key)
  category.delete()
  return redirect('category')
    




def add_post(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    doctor = Doctor.objects.get(User_Master=user)
    if request.method=="POST":  
        title = request.POST['Title']
        image = request.FILES['image1'] 
        category1 = request.POST['Category']
        summary = request.POST['Summary']
        content = request.POST['Content']
        
        category = Category.objects.get(Category_name=category1)
        datetime1 = datetime.datetime.now()
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        doctor = Doctor.objects.get(User_Master=user)
        if 'draft' in request.POST:
            draft = True
        else:
            draft = False

        new_post = Post.objects.create(
            Doctor=doctor,
            Title=title,
            Image=image,
            Category=category,
            Summary=summary,
            Content=content,
            DateTimeOfPoast=datetime1,
            Draft=draft
            )
        
        return redirect('posts')

    else:
        category = Category.objects.filter(Doctor=doctor)
        data = {
            'category':category
        }
        return render(request,"doctor/add_post.html",data)

def posts(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    doctor = Doctor.objects.get(User_Master=user)
    request.session['pic']=doctor.Profile_Picture.url
    request.session['fname']=doctor.First_Name
    request.session['lname']=doctor.Last_Name

    posts = Post.objects.filter(Doctor=doctor)
    paginator = Paginator(posts,5)
    page = request.GET.get('page')
    paged_post = paginator.get_page(page)
    data = {
        'post':paged_post
    }
    return render(request,"doctor/posts.html",data)


def update_post(request,key):
  post = Post.objects.get(id=key)
  if request.method=="POST":
        title = request.POST['Title']
        image = request.FILES['image1'] 
        category1 = request.POST['Category']
        summary = request.POST['Summary']
        content = request.POST['Content']
        
        category = Category.objects.get(Category_name=category1)
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        doctor = Doctor.objects.get(User_Master=user)
        if 'draft' in request.POST:
            post.Draft = True
        else:
            post.Draft = False
        post.Title = title
        post.Image = image
        post.Category = category
        post.Summary = summary
        post.Content = content
        post.save()
        return redirect('posts')
        

  else:
    category = Category.objects.all()
    data = {
        'post':post,
        'category':category

    }
    print(post)
    return render(request,"doctor/update_post.html",data)

def delete_post(request,key):
  post = Post.objects.get(id=key)
  post.delete()
  return redirect('posts')



def index(request):
   
        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        patient = Patient.objects.get(User_Master=user)
        request.session['pic']=patient.Profile_Picture.url
        request.session['fname']=patient.First_Name
        request.session['lname']=patient.Last_Name
        
        try:
            category_name = request.GET.get('category')
            category = Category.objects.get(Category_name=category_name)
            post = Post.objects.filter(Category=category,Draft=False)
        except:
            post = Post.objects.filter(Draft=False)
        paginator = Paginator(post,3)
        page = request.GET.get('page')
        paged_post = paginator.get_page(page)
        category = Category.objects.all()
        data = {
            'post':paged_post,
            'category':category,
        }
        print(category)
        return render(request,"patient/index.html",data)
    

def single_post(request,key):
    post = Post.objects.get(id=key)
    print(post)
    data = {
        'post':post,
    }
    return render(request,"patient/single_post.html",data)


    
def doctors(request):
    doctor =Doctor.objects.all()
    paginator = Paginator(doctor,3)
    page = request.GET.get('page')
    paged_doctor = paginator.get_page(page)  
    data = {
        'doctor' : paged_doctor
    }
    return render(request,"patient/doctors.html",data)

def book_appointment(request):
    if request.method=="POST":
        required_speciality = request.POST['required_speciality']
        date_of_appointment = request.POST['date_of_appointment']
        start_time_of_appointment = request.POST['start_time_of_appointment'] 
        contect = request.POST['contect']
        doctor_id = request.POST['doctor_id']


        id=request.session.get("id")
        user = User_Master.objects.get(id=id)
        patient = Patient.objects.get(User_Master=user)
        doctor =Doctor.objects.get(id=doctor_id)
        

       
        temp = date_of_appointment+" "+start_time_of_appointment+":0.00"
        date_time_obj = datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f')
        start = date_time_obj
        end = date_time_obj + timedelta(minutes=45)
        end_time_of_appointment = end.time()
        
        
        data = {
            'doctor_id' : doctor_id
        }
        
        GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client_secret.json')
        scopes = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file(GDRAT_abs_path, scopes=scopes)
        credentials = flow.run_local_server()
        service = build("calendar", "v3", credentials=credentials)

        event_request_body = {
            'start' : {
                'dateTime' : start.isoformat(),
                'timeZone' : 'Asia/Kolkata'
            },
            'end' : {
                'dateTime' : (start + timedelta(minutes=45)).isoformat(),
                'timeZone' : 'Asia/Kolkata'
            },
            'summary' : 'Doctor Appointment',
            'description' : doctor.First_Name + " "+ doctor.Last_Name + "'s Appointment",
            'colorId' : '4',
            'status' : 'confirmed',
            
        }
        response3 = service.events().insert(
            calendarId='primary', body=event_request_body
        ).execute()

        new_appointment = Appointment.objects.create(
            Patient = patient,
            Doctor = doctor,
            Required_speciality = required_speciality,
            Date_of_Appointment = date_of_appointment,
            Start_Time_of_Appointment = start_time_of_appointment,
            End_Time_of_Appointment = end_time_of_appointment,
            Contect = contect
        )

        return redirect('patient_appointments')
    else:

        doctor_id = request.GET.get('id')
        data = {
            'doctor_id' : doctor_id
        }

        return render(request,"patient/book_appointment.html",data)



def patient_appointments(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    patient = Patient.objects.get(User_Master=user)
    appointment = Appointment.objects.filter(Patient=patient)

    paginator = Paginator(appointment,3)
    page = request.GET.get('page')
    paged_appointment = paginator.get_page(page)
    print(appointment)
    
    data = {
        'appointment':paged_appointment
    }
    return render(request,"patient/patient_appointments.html",data)

def doctor_appointments(request):
    id=request.session.get("id")
    user = User_Master.objects.get(id=id)
    doctor = Doctor.objects.get(User_Master=user)
    appointment = Appointment.objects.filter(Doctor=doctor) 
    paginator = Paginator(appointment,5)
    page = request.GET.get('page')
    paged_appointment = paginator.get_page(page)   
    data = {
        'appointment':paged_appointment
    }
    return render(request,"doctor/doctor_appointments.html",data)
    

def doctor_appointments_detail(request):
    appointment_id = request.GET.get('id')
    appointment = Appointment.objects.get(id=appointment_id)
    data = {
        'appointment':appointment
    }
    return render(request,"doctor/doctor_appointments_detail.html",data)


def Confirm_appointment(request):
    appointment_id = request.GET.get('id')
    appointment = Appointment.objects.get(id=appointment_id)
   
    print("----------------------------------")

    start = datetime(
        appointment.Date_of_Appointment.year,
        appointment.Date_of_Appointment.month,
        appointment.Date_of_Appointment.day,
        appointment.Start_Time_of_Appointment.hour,
        appointment.Start_Time_of_Appointment.minute,
        appointment.Start_Time_of_Appointment.second,
        appointment.Start_Time_of_Appointment.microsecond,


    )
    
    GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'client_secret.json')
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file(GDRAT_abs_path, scopes=scopes)
    credentials = flow.run_local_server()
    service = build("calendar", "v3", credentials=credentials)

    event_request_body = {
            'start' : {
                'dateTime' : start.isoformat(),
                'timeZone' : 'Asia/Kolkata'
            },
            'end' : {
                'dateTime' : (start + timedelta(minutes=45)).isoformat(),
                'timeZone' : 'Asia/Kolkata'
            },
            'summary' : 'Patient Appointment',
            'description' : appointment.Patient.First_Name + " "+ appointment.Patient.Last_Name + "'s Appointment",
            'colorId' : '4',
            'status' : 'confirmed',
            
    }
    response3 = service.events().insert(
            calendarId='primary', body=event_request_body
    ).execute()
    
    appointment.Status = "Confirmed"
    appointment.save()
   
    return redirect('doctor_appointments')