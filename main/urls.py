from django.urls import path
from main.views import show_main, login_user,register_buyer
app_name = 'main'

urlpatterns = [
    path('',show_main,name='show_main'),
    path('login/',login_user,name="login_user"),
    path('register/buyer',register_buyer,name="register_buyer")
]