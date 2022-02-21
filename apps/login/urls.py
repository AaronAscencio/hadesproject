from unicodedata import name
from django.urls import path
from apps.login.views import *

app_name = 'login'


urlpatterns = [
    path('login/',LoginFormView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),

]
