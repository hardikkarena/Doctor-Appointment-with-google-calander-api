from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone
# Create your models here.

class User_Master(models.Model):
    Username = models.CharField(max_length=20)
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=300)
    Role = models.CharField(max_length=20)

    def __str__(self):
        return self.Email

class Patient(models.Model):
    User_Master = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30)
    Profile_Picture = models.ImageField(upload_to='Profile_Pics',default="user.png")
    Address = models.CharField(max_length=300)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pin_Code = models.IntegerField()

    def __str__(self):
        return self.First_Name

class Doctor(models.Model):
    User_Master = models.ForeignKey(User_Master,on_delete=models.CASCADE)
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30)
    Profile_Picture = models.ImageField(upload_to='Profile_Pics',default="user.png")
    Address = models.CharField(max_length=300)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Pin_Code = models.IntegerField()

    def __str__(self):
        return self.First_Name

class Category(models.Model):
    Category_name = models.CharField(max_length=150)
    Doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)


    def __str__(self):
        return self.Category_name

class Post(models.Model):
    Doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Title = models.CharField(max_length=150)
    Image = models.ImageField(upload_to='Post_Images',)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Summary = models.CharField(max_length=500)
    Content = models.CharField(max_length=1000)
    DateTimeOfPoast = models.DateTimeField()
    Draft = models.BooleanField(default=False)
    def __str__(self):
        return self.Title

    class Meta:
        ordering = ['-DateTimeOfPoast']

class Appointment(models.Model):
    Patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    Doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Required_speciality = models.CharField(max_length=150)
    Date_of_Appointment = models.DateField()
    Start_Time_of_Appointment = models.TimeField()
    End_Time_of_Appointment = models.TimeField()
    Contect = models.BigIntegerField()
    Status = models.CharField(max_length=20,default="Pending")

 







