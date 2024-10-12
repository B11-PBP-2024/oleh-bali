from django.urls import path
from main.views import show_main, login_buyer
app_name = 'main'

urlpatterns = [
    path('',show_main,name='show_main'),
    path('login/buyer',login_buyer,name="login_buyer")
]