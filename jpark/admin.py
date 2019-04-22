from django.contrib import admin
from .models import Profile, Parking, Reservation, Category

class ProfileAdmin(admin.ModelAdmin):  # add this
  list_display = ('user', 'first_name', 'completed')
      # list_display = ('user', 'first_name', 'last_name','licence_plate', 'email', 'phone', 'balance', 'completed') # add this


# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Parking)
admin.site.register(Reservation)
admin.site.register(Category)
