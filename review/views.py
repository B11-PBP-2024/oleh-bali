from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from review.models import ReviewEntry
from seller.models import ProductEntry
from review.forms import ReviewEntryForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def show_review(request,id):
    product = ProductEntry.objects.get(pk=id)
    reviews = ReviewEntry.objects.filter(product=product).select_related('user', 'user__buyerprofile')
    context= {
        'reviews':reviews,
        'product':product
    }
    return render(request, "review_page.html", context)

def create_review(request,id):
    form = ReviewEntryForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        review = form.save(commit=False)
        review.user = request.user
        product = ProductEntry.objects.get(pk=id)
        review.product = product
        review.review_text = review.review_text.replace("/r","/n")
        review.save()
        return redirect('review:show_review', id=product.id)
    
    context = {'form': form}
    return render(request, "create_review.html", context)

def edit_review(request,id):
    review = ReviewEntry.objects.get(pk=id)

    form = ReviewEntryForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review:show_review', args=[review.product.id]))
    
    context = {'form': form}
    return render(request, "edit_review.html", context)

def delete_review(request,id):
    review = ReviewEntry.objects.get(pk=id)
    product_id = review.product.id
    print(product_id)

    review.delete()

    return HttpResponseRedirect(reverse('review:show_review', args=[product_id]))

# @csrf_exempt
# @require_POST
# def create_review_ajax(request):
#     review = request.POST.get("review")
#     user = request.user

