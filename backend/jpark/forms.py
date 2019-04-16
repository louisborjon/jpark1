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
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2')

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
        'username',
        'first_name',
        'last_name',
        'email')
