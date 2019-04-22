"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from jpark.views import signup_view, login_view, edit_profile_view, root, starting_page,mainpage, profile_view, change_password, user_logout, reservations, search, about_us_view, list_view
from rest_framework import routers
from jpark import views

router = routers.DefaultRouter()
router.register(r'profiles', views.ProfileView, 'jpark')
# router.register(r'todos', views.CategoryView, 'jpark'),
# router.register(r'todos', views.ParkingView, 'jpark'),
# router.register(r'todos', views.ReservationView, 'jpark'),


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('signup/', signup_view, name='signup'),
    path('home/ ', starting_page, name="home"),
    path('', root, name="root"),

    path('editprofile/', edit_profile_view, name='editprofile'),
    path('login/', login_view, name='login'),
    path('mainpage/', mainpage, name='mainpage'),
    path('search/', search, name='search'),

    path('profile/<int:id>', profile_view, name="profile"),
    path('password/', change_password, name='change_password'),
    path('logout/', user_logout, name='logout'),
    path('reservations/', reservations, name='reservations'),
    path('list/', list_view, name="list"),
    path('about_us/', about_us_view, name ='about_us'),
]
