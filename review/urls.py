from django.urls import path
from review.views import show_review, create_review

app_name = "review"

urlpatterns = [
    path('<uuid:id>', show_review, name='show_review'),
    path('create/<uuid:id>', create_review, name='create_review'),
    
    
]