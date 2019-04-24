from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib import messages
from jpark.models import  Category, Parking, Reservation
from django.http import HttpResponse, HttpResponseRedirect


from jpark.forms import LoginForm, EditProfileForm, addSpotForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework import viewsets
from .serializers import ProfileSerializer, CategorySerializer, ParkingSerializer, ReservationSerializer

from .models import Category, Parking, Reservation, CustomUser
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm







class ProfileView(viewsets.ModelViewSet):
  serializer_class = ProfileSerializer
  queryset = CustomUser.objects.all()

class CategoryView(viewsets.ModelViewSet):
  serializer_class = CategorySerializer
  queryset = Category.objects.all()

class ParkingView(viewsets.ModelViewSet):
  serializer_class = ParkingSerializer
  queryset = Parking.objects.all()

class ReservationView(viewsets.ModelViewSet):
  serializer_class = ReservationSerializer
  queryset = Reservation.objects.all()

# Create your views here.
def starting_page(request):
    return render(request, 'home.html')

def root(request):
    return render(request, 'home.html')

@login_required
def reservations(request):
    return render(request, 'reservations.html')

@login_required
def mainpage(request):
    return render(request, 'mainpage.html')

@login_required
def search(request):
    return render(request, 'search.html')


def about_us_view(request):
    return render(request, 'about_us.html')

#class SignUp(generic.CreateView):
    #form_class = CustomUserCreationForm
    #success_url = reverse_lazy('login')
    #template_name = 'signup.html'


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            #user.groups.add(Group.objects.get(name='Owners'))
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/profileinfo/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form':form})

         #profile_form.save()
          #  license_plate = form.cleaned_data.get('license_plate')
           # phone_number = form.cleaned_data.get('phone_number')
        #profile_form = ProfileForm(request.POST)


#Profile Info Form
def ProfileInfo_view(request):
    pass



@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            user = form.instance
            return redirect('/profile/{}'.format(user.profile.pk)) #will redirect to Profile page
    else:
        form = EditProfileForm(instance=request.user)
    args = {'form':form}
    return render(request, 'editprofile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to hash passwords
            messages.success(request, 'Your password was changed successfully!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('home'))


def login_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('/home/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password= password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/mainpage/')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    context = {'form': form}
    response = render(request, 'login.html', context)
    return HttpResponse(response)

@login_required
def profile_view(request, id):
    profile = CustomUser.objects.get(pk=id)
    parking = Parking.objects.get(pk=id)
    context = {
        'profile': profile,
        'parking': parking
       # 'reservations':reservation
        }

    return render(request, 'profile.html', context)

def is_Owner(user):
    return user.groups.filter(name='Owner').exists()


@login_required
#@permission_required('jpark.can_view_parking')
def list_view(request):
        return render(request, 'list.html')



@login_required
def delete_parking(request, id):
    Parking = Parking.objects.get(pk=id)
    Parking.delete()
    return render(request, 'home.html')


@login_required
def add(request):
    if request.method == "POST":
        form = addSpotForm(request.POST)
        form.instance.owner = request.user
        if form.is_valid():
                add_form = form.save(commit=False)
                add_form.save()
                return redirect('/mainpage/')
        else:
            form = addSpotForm()
    else: 
        form = addSpotForm()
    return render(request, 'addspot.html', {'form':form})

@login_required
def delete(request):
    Parking = Parking.objects.get(pk=id)
    Parking.delete()
    return render(request, 'deletespot.html')

#make validation to check for plate number and phone number fields. if they don't prompt them to add those fields in order to add parking spot.