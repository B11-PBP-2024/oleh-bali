from django.urls import path
from main.views import show_main,login_buyer,login_seller, register_buyer, register_seller, logout_user
app_name = 'main'

urlpatterns = [
    path("",show_main,name="show_main"),
    path("login/buyer",login_buyer,name="login_buyer"),
    path("register/buyer",register_buyer,name="register_buyer"),
    path("login/seller",login_seller,name="login_seller"),
    path("register/seller",register_seller,name="register_seller"),
    path("logout/",logout_user,name="logout_user")
]