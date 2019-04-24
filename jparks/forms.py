from django.forms import CharField, PasswordInput, Form
from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from jparks.models import Parking, Reservation, CustomUser

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())


class addSpotForm(forms.ModelForm):
    street_type = forms.CharField(max_length=4)
    street_name = forms.CharField(max_length=255)
    street_number = forms.IntegerField()
    zip_code = forms.CharField(max_length=6)
    province = forms.CharField(max_length=255)
    city = forms.CharField(max_length=255)
    image = forms.URLField(max_length=255)
    phone = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    opening_time = forms.TimeField()
    closing_time = forms.TimeField()
    hourly_rate = forms.IntegerField()

    class Meta():
        model = Parking
        fields = (
        'street_type', 
        'street_name',
        'street_number', 
        'zip_code', 
        'province', 
        'city', 
        'image', 
        'phone',
        'description',
        'opening_time', 
        'closing_time',  
        'hourly_rate'  
            )


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'license_plate', 'phone_number')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'license_plate', 'first_name', 'last_name')

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
        'username',
        'first_name',
        'last_name',
        'email')

class ReservationForm(forms.ModelForm):
    starting_date = forms.DateField()
    ending_date = forms.DateField()
    starting_time = forms.DateField()
    ending_time = forms.DateField()
    created_at = forms.DateField()
    notes = forms.Textarea()
    Parking = forms.CharField(max_length=121)
    class Meta():
        model = Reservation
        fields = (
            'Parking', 
            'ending_date',
            'starting_time',
            'ending_time',
            'notes')


