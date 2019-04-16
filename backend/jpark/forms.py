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
    email = forms.EmailField(max_length=255)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            )

class EditProfileForm(UserChangeForm):
    first_name = forms.Charfield(max_length=255)
    last_name = forms.CharField(max_length=255)
    licence_plate = forms.CharField(max_length=255)
    email = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=255, null=True)
    user = forms.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    balance = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'licence_plate',
        'phone',
        'balance',

        )
