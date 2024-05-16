"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from mysite.views import (
    HomePageView,
    AccountPageView,
    MoviePageView,
    RentPageView,
    UserManager,
    MovieManager,
    RentalManager,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("account/", AccountPageView.as_view(), name="account"),
    path('admin/', admin.site.urls),
    path("movie/", MoviePageView.as_view(), name="movie"),
    path("rent/", RentPageView.as_view(), name="rent"),
    path("dbUser/", UserManager.as_view(), name="dbUser"),
    path("dbMovie/", MovieManager.as_view(), name="dbMovie"),
    path("dbRent/", RentalManager.as_view(), name="dbRent"),
    path('create_user/', UserManager.as_view(), name='create_user'),
    path('add_movie/', MovieManager.as_view(), name='add_movie'),
    path('rent_movie/', RentalManager.as_view(), name='rent_movie')
]
