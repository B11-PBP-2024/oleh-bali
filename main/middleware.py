# article/middleware.py
from django.shortcuts import redirect,render
from django.urls import resolve

class AuthenticationAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and resolve(request.path_info).app_name in 'article katalog like review see_stores store wishlist seller':
            return redirect("main:login_buyer")
        if request.user.is_authenticated and resolve(request.path_info).app_name in 'article katalog like review see_stores store wishlist' and request.user.role != 0:
            return render(request,"403.html")
        if request.user.is_authenticated and 'seller' in resolve(request.path_info).app_name and request.user.role == 0:
            return render(request,"403.html")
        print(resolve(request.path_info))
        return self.get_response(request)
