from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib import messages
from jpark.models import Profile, Category, Parking, Reservation
from django.http import HttpResponse, HttpResponseRedirect
from jpark.forms import LoginForm, SignupForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def root(request):
    return render(request, 'home.html')

def reservations(request):
    return render(request, 'reservations.html')

def mainpage(request):
    return render(request, 'mainpage.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/home/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form':form})

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


def profile_view(request, id):
    profile = Profile.objects.get(pk=id)
    context = {
        'profile': profile,
       # 'reservations':reservation
        }

    return render(request, 'profile.html', context)
