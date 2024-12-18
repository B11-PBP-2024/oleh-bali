"""
URL configuration for oleh_bali project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from main.views import view_404 

handler404 = 'main.views.view_404'
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include("main.urls")),
    path("article/",include("article.urls")),
    path('review/', include('review.urls')),
    path("products/",include("seller.urls")),
    path("catalog/",include("katalog.urls")),
    path("store/",include("store.urls")),
    path("wishlist/",include("wishlist.urls")),
    path("profile/",include("user_profile.urls")),
    path('like/', include('like.urls')),
    path('see_stores/', include('see_stores.urls', namespace='see_stores')),

]
