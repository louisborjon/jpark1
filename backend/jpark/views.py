from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def root(request):
    return render(request, 'home.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

