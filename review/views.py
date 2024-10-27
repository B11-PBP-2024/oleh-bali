from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from review.models import ReviewEntry
from seller.models import ProductEntry
from review.forms import ReviewEntryForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator

def show_review(request,id):
    product = ProductEntry.objects.get(pk=id)
    reviews = ReviewEntry.objects.filter(product=product).select_related('user', 'user__buyerprofile')
    context= {
        'reviews':reviews,
        'product':product
    }
    return render(request, "review_page.html", context)

# @csrf_exempt
def create_review(request, id):
    if request.method == "POST":
        form = ReviewEntryForm(request.POST or None)

        # Debug: Print the POST data
        print("POST data:", request.POST)
        
        # Cek apakah form valid
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            product = ProductEntry.objects.get(pk=id)
            review.product = product
            review.review_text = review.review_text.replace("\r", "\n")  # Format line break dengan benar
            review.save()

            # Cek apakah request adalah AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": True})
            else:
                return redirect('review:show_review', id=product.id)
        else:
            # Debug untuk error form jika form tidak valid
            print("Form errors:", form.errors)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})

    # Render form jika GET atau permintaan POST tidak valid
    form = ReviewEntryForm()
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
