from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.hashers import make_password,check_password
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
        elif new_user.Role == 'Patient':
            new_doctor = Patient.objects.create(
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
    return redirect('dashboard')
    
    
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
                return redirect('dashboard')

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
        return render(request,"doctor_dashboard.html",data)
    else:
        patient = Patient.objects.get(User_Master=user)
        request.session['pic']=patient.Profile_Picture.url
        request.session['fname']=patient.First_Name
        request.session['lname']=patient.Last_Name
        data = {
            'user':user,
            'doctor':patient
        }
        return render(request,"doctor_dashboard.html",data)
def Logout(request):
    del request.session['id']
    del request.session['fname']
    del request.session['lname']
    del request.session['pic']
    return redirect('login')


    
        
