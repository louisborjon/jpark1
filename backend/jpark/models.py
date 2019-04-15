from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    licence_plate = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    balance = models.CharField(max_length=255)


    def __str__(self):
        return self.full_name()

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def exists_for_user(self, user):
        return Profile.objects.filter(user_id=user.id).exists()


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def location(self):
        return self.parking_lots.all()[0].location

class Parking(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_parking_lots')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='parking_lots')
    guests = models.ManyToManyField(User, through='Reservation', related_name='reserved_parking_lots')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.URLField(max_length=255, null=True)
    description = models.TextField(null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    price = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def parking_past_midnight(self):
        return self.closing_time < self.opening_time

    def time_frame(self, date, starting_time, ending_time):
        reserved_parking = self.reservations.filter(date=date, starting_time=starting_time, ending_time=ending_time).aggregate(Sum('reserved_time'))
        reserved_parking = reserved_parking['reserved_time__sum'] or 0
        return (reserved_parking + starting_time) <= self.availability

class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservations_made', on_delete=models.CASCADE)
    parking = models.ForeignKey(Parking, related_name='reservations', on_delete=models.CASCADE)
    date = models.DateField()
    starting_time = models.TimeField()
    reserved_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)


    def __str__(self):
        return "{} {} - Reserved Time {}".format(self.date, self.time, self.reserved_time)

    def date_and_time(self):
        date = self.date.strftime("%Y-%m-%d")
        starting_time = self.starting_time.strftime("%H:%M")
        ending_time = self.ending_time.strftime("%H:%M")
        return "{} {} {}".format(date, starting_time, ending_time)
