from django.shortcuts import render

# Create your views here

def show_review(request):
    return render(request, "review_page.html")
