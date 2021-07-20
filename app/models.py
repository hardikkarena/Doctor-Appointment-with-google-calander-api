from django.db import models
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

