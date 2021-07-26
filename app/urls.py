from django.urls import path,include
from . import views
urlpatterns = [
path("singup/",views.Singup,name="singup"),
path("",views.Login,name="login"),
path("submit_data/",views.Submit_data,name="submit_data"),
path("Dashboard/",views.Dashboard,name="dashboard"),
path("logout/",views.Logout,name="logout"),
path("temp/",views.temp,name="temp"),

#category Views
path("category/",views.category,name="category"),
path("add_category/",views.add_category,name="add_category"),
path("update_category/<int:key>",views.update_category,name="update_category"),
path("delete_category/<int:key>",views.delete_category,name="delete_category"),


path("posts/",views.posts,name="posts"),
path("add_post/",views.add_post,name="add_post"),
path("update_post/<int:key>",views.update_post,name="update_post"),
path("add_post/<int:key>",views.delete_post,name="delete_post"),

path("index/",views.index,name="index"),
path("single_post/<int:key>",views.single_post,name="single_post"),

path("doctors/",views.doctors,name="doctors"),
path("book_appointment/",views.book_appointment,name="book_appointment"),
path("patient_appointments/",views.patient_appointments,name="patient_appointments"),
path("doctor_appointments/",views.doctor_appointments,name="doctor_appointments"),
path("doctor_appointments_detail/",views.doctor_appointments_detail,name="doctor_appointments_detail"),
path("Confirm_appointment/",views.Confirm_appointment,name="Confirm_appointment")





]
