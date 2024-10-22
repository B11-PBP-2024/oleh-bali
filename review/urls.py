from django.urls import path
from review.views import show_review

app_name = "review"

urlpatterns = [
    path('<uuid:id>', show_review, name='show_review')
]