from django.contrib import admin
from .models import User_Master,Doctor,Patient
# Register your models here.

@admin.register(User_Master)
class User_Master_admin(admin.ModelAdmin):
    list_display = ['Username','Email','Role']

@admin.register(Doctor)
class Doctor_admin(admin.ModelAdmin):
    list_display = ['First_Name','Last_Name']

@admin.register(Patient)
class Patient_admin(admin.ModelAdmin):
    list_display = ['First_Name','Last_Name']

