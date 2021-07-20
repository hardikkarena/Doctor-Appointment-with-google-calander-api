from django.urls import path,include
from . import views
urlpatterns = [
path("singup/",views.Singup,name="singup"),
path("",views.Login,name="login"),
path("submit_data/",views.Submit_data,name="submit_data"),
path("Dashboard/",views.Dashboard,name="dashboard"),
path("logout/",views.Logout,name="logout"),


]
