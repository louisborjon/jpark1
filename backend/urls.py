
from django.contrib import admin
from django.urls import path, include
from jpark.views import signup_view, login_view, edit_profile_view, root, starting_page,mainpage, profile_view, change_password, user_logout, reservations, search, about_us_view, list_view
from jpark.views import add, delete
from rest_framework import routers
from jpark import views

router = routers.DefaultRouter()
router.register(r'parking', views.ParkingView, 'jpark')
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
    path('deletespot', delete, name='delete'),
    path('addspot/', add, name='add'),

    path('profile/<int:id>', profile_view, name="profile"),
    path('password/', change_password, name='change_password'),
    path('logout/', user_logout, name='logout'),
    path('reservations/', reservations, name='reservations'),
    path('list/', list_view, name="list"),
    path('about_us/', about_us_view, name ='about_us'),
]
