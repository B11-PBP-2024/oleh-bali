from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
from django.contrib import messages

# Create your views here.

def show_main(request):
    user = request.user
    if user.is_seller():
        return render(request,'homepage_seller.html')
    else:
        return render(request,'homepage_buyer.html')

def login_buyer(request):
    if request.method == "POST":
        
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            if user.is_seller():
                messages.error(request,"User is not registered as Buyer!")
            else:
                login(request,user)
                return redirect('show_main')
        else:
            messages.error(request,"Invalid username or password!")
    else:
        form = AuthenticationForm()
    
    context = {
        'form' : form,
    }
    return render(request,"login/login.html",context)
