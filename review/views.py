from django.shortcuts import render
from review.models import ReviewEntry
from seller.models import ProductEntry

# Create your views here

def show_review(request,id):
    product = ProductEntry.objects.get(pk=id)
    reviews = ReviewEntry.objects.filter(product=product)
    context= {
        'reviews':reviews,
        'product':product
    }
    return render(request, "review_page.html", context)
