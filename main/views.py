from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,authenticate, get_user_model,logout
from django.contrib import messages
from .forms import CustomBuyerCreationForm, CustomSellerCreationForm, CustomAuthenticationForm
from user_profile.models import BuyerProfile, SellerProfile
import json
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()
# Create your views here.

def view_404(request, exception=None):
    return render(request, '404.html', status=404)

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
            profile_buyer, created = BuyerProfile.objects.get_or_create(user=user) 
            if created:
                profile_buyer.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
                profile_buyer.store_name = user.username 
                profile_buyer.nationality = "Not Set"  
                profile_buyer.save()  
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
            profile_seller, created = SellerProfile.objects.get_or_create(user=user) 
            if created:
                profile_seller.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
                profile_seller.store_name = user.username 
                profile_seller.city = "Denpasar"  
                profile_seller.subdistrict = "Denpasar Selatan"
                profile_seller.village = "Panjer"
                profile_seller.address = "Not Set"  
                profile_seller.maps = "https://www.google.com/maps"  
                profile_seller.save() 
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
    
def show_wishlist(request):
    return render(request, 'wishlist/wishlist.html')



@csrf_exempt
def login_buyer_mobile(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if user.role == 0:
                auth_login(request, user)
                # Status login sukses.
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login sukses!"
                    # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
                }, status=200)
            else:
                return JsonResponse({
                "status": False,
                "message": "Login gagal, akun bukan seorang buyer."
            }, status=401)

        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def login_seller_mobile(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if user.role == 1:
                auth_login(request, user)
                # Status login sukses.
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login sukses!"
                    # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
                }, status=200)
            else:
                return JsonResponse({
                "status": False,
                "message": "Login gagal, akun bukan seorang Seller."
            }, status=401)

        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def register_buyer_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.role = 0
        user.save()
        profile_buyer, created = BuyerProfile.objects.get_or_create(user=user) 
        if created:
            profile_buyer.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
            profile_buyer.store_name = user.username 
            profile_buyer.nationality = "Not Set"  
            profile_buyer.save()  
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
@csrf_exempt
def login_seller_mobile(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            if user.role == 1:
                auth_login(request, user)
                # Status login sukses.
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login sukses!"
                    # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
                }, status=200)
            else:
                return JsonResponse({
                "status": False,
                "message": "Login gagal, akun bukan seorang Seller."
            }, status=401)

        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def register_seller_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.role = 1
        user.save()
        profile_seller, created = SellerProfile.objects.get_or_create(user=user) 
        if created:
            profile_seller.profile_picture = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
            profile_seller.store_name = user.username 
            profile_seller.city = "Denpasar"  
            profile_seller.subdistrict = "Denpasar Selatan"
            profile_seller.village = "Panjer"
            profile_seller.address = "Not Set"  
            profile_seller.maps = "https://www.google.com/maps"  
            profile_seller.save() 
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    
@csrf_exempt
def logout_mobile(request):
    username = request.user.username

    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
