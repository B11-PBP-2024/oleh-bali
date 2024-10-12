from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,authenticate, get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm

# Create your views here.
User = get_user_model()

def show_main(request):
    user = request.user
    if user.is_seller():
        return render(request,'homepage_seller.html')
    else:
        return render(request,'homepage_buyer.html')

def login_user(request):
    if request.method == "POST":
        
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            
            login(request,user)
            return redirect('show_main')
        else:
            messages.error(request,"Invalid username or password!")
    else:
        form = AuthenticationForm()
    
    context = {
        'form' : form,
    }
    return render(request,"auth/login.html",context)

def register_buyer(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller = False
            user.save()
            return redirect('login_user')
    else:
        form = CustomUserCreationForm()
    
    return render(request, "auth/register_buyer.html", {'form':form})
    
