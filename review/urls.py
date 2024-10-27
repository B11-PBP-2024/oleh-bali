from django.urls import path
from review.views import show_review, create_review, edit_review, delete_review

app_name = "review"

urlpatterns = [
    path('<uuid:id>', show_review, name='show_review'),
    path('create/<uuid:id>', create_review, name='create_review'),
    path('edit-review/<uuid:id>', edit_review, name='edit_review'),
    path('delete/<uuid:id>', delete_review, name='delete_review'),
]