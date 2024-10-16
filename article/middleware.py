# article/middleware.py
from django.shortcuts import redirect
from django.urls import resolve

class BuyerRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and resolve(request.path_info).app_name == 'article':
            return redirect('/login/buyer')
        if request.user.is_authenticated and resolve(request.path_info).app_name == 'article' and request.user.role != 0:
            return redirect('/')
        return self.get_response(request)
