from django.forms import CharField, PasswordInput, Form
from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())


class SignupForm(UserCreationForm):
    first_name = CharField(max_length=244)
    last_name = CharField(max_length=244)
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username', 
            'email'
            )
    
    
    #def __str__(self):
        #return self.first_name

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
        'username',
        'first_name',
        'last_name',
        'email')

class ListForm(Form):
    pass
