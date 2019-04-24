from rest_framework import serializers
from .models import Profile, Category, Parking, Reservation

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('user', 'first_name', 'last_name ', 'licence_plate', 'email', 'phone', 'balance')

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
   model = Category
   fields = ('zone_in_category_choices', 'zone_price')

class ParkingSerializer(serializers.ModelSerializer):
  class Meta:
   model = Parking
   fields = ('owner', 'drivers', 'street_type', 'street_name', 'street_number', 'zip_code', 'province', 'city', 'image', 'phone', 'description', 'opening_time', 'closing_time', 'hourly_rate', 'lat', 'lng')

class ReservationSerializer(serializers.ModelSerializer):
  class Meta:
   model = Reservation
   fields = ('Profile', 'parking', 'starting_date', 'ending_date', 'starting_time', 'ending_time', 'created_at', 'notes')
