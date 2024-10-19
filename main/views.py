from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,authenticate, get_user_model,logout
from django.contrib import messages
from .forms import CustomBuyerCreationForm, CustomSellerCreationForm, CustomAuthenticationForm
User = get_user_model()
# Create your views here.
@login_required(login_url="login/buyer")
def show_main(request):
    if request.user.role == 1:
        return render(request,"homepage_seller.html")
    return render(request,"homepage_buyer.html")

def login_buyer(request):
    form = AuthenticationForm()
    debug = "NO"
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            debug = "YES"
            user = form.get_user()
            if user.role == 1:
                messages.error(request,"Not registered as a buyer!")
            else:
                login(request,user)
                return redirect("main:show_main")
    else:
        form = AuthenticationForm()
    context = {'form':form, 'debug':debug}
    return render(request,"auth/login_buyer.html",context)

def register_buyer(request):
    form = CustomBuyerCreationForm()
    debug = "no"
    if request.method == "POST":
        form = CustomBuyerCreationForm(request.POST)
        if form.is_valid():
            debug="yes"
            user = form.save(commit=False)
            user.role = 0
            user.save()
            messages.success(request,message="Your account has been successfully created!")
            return redirect("main:login_buyer")
    context = {'form':form}
    return render(request,"auth/register_buyer.html",context)

def login_seller(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 0:
                messages.error(request,"Not registered as a seller!")
            else:
                login(request,user)
                return redirect("main:show_main")
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request,"auth/login_seller.html",context)

def register_seller(request):
    form = CustomSellerCreationForm()
    if request.method == "POST":
        form = CustomSellerCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 1
            user.save()
            messages.success(request,message="Your account has been successfully created!")
            return redirect("main:login_seller")
    context = {'form':form,}
    return render(request,"auth/register_seller.html",context)

def logout_user(request):
    role = request.user.role
    logout(request)
    if role == 0:
        return redirect("main:login_buyer")
    else:
        return redirect("main:login_seller")
    