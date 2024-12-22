from django.urls import path
from review.views import delete_review_mobile, edit_review_mobile, show_review, create_review, edit_review, delete_review, get_reviews

app_name = "review"

urlpatterns = [
    path('<uuid:id>', show_review, name='show_review'),
    path('create/<uuid:id>', create_review, name='create_review'),
    path('edit-review/<uuid:id>', edit_review, name='edit_review'),
    path('edit-review/mobile/<uuid:id>', edit_review_mobile, name='edit_review_mobile'),
    path('delete/<uuid:id>', delete_review, name='delete_review'),
    path('json/<uuid:id>', get_reviews, name='get_reviews'),
    path('delete/mobile/<uuid:id>', delete_review_mobile, name='delete_review_mobile'),
]