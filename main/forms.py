from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from main.models import User,Buyer,Seller

class CustomBuyerCreationForm(UserCreationForm):
    class Meta:
        model = Buyer
        fields = ('username', 'password1', 'password2')

class CustomSellerCreationForm(UserCreationForm):
    class Meta:
        model = Seller
        fields = ('username', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')



