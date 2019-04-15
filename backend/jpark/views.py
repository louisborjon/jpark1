from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from jpark.models import Profile, Category, Parking, Reservation

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

def edit_profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('') #will redirect to Profile page
    else:
        form = UserChangeForm()
        args = {'form':form}
        return render(request, 'editprofile.html', args)
