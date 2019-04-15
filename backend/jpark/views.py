from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from jpark.forms import LoginForm

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password= password)
            login(request, user)
            redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

def login_view(request):
 if request.user.is_authenticated:
        return HttpResponseRedirect('signup_view')
 if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password= password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('signup_view')
            else:
                form.add_error('username', 'Login failed')
 else:
        form = LoginForm()

 context = {'form': form}
 response = render(request, 'login.html', context)
 return HttpResponse(response)
