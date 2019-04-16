from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    licence_plate = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
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
    """ Category respresenting zone price """
    zone_1 = 'Z1'
    zone_2 = 'Z2'
    zone_3 = 'Z3'
    zone_in_category_choices = (
        (zone_1, 'zone_1'),
        (zone_2, 'zone_2'),
        (zone_3, 'zone_3'),
    )
    zone_price = models.CharField(max_length=2, choices=zone_in_category_choices, default=zone_1)

    def __str__(self):
        return self.zone_price

    def location(self):
        return self.parking_lots.all()[0].hourly_rate

class Parking(models.Model):
    CHOICES_IN_STREET_TYPES = (
        ('ST', 'Street'),
        ('AVE', 'Avenue'),
        ('BLVD', 'Boulevard'),
    );
    PROVINCE_CHOICES = (
        ('BC', 'British Columbia'),
        ('MB', 'Manitoba'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NT', 'Northwest Territories'),
        ('NS', 'Nova Scotia'),
        ('NU', 'Nunavut'),
        ('ON', 'Ontario'),
        ('PE', 'Prince Edward Island'),
        ('QC', 'Québec'),
        ('SK', 'Saskatchewan'),
        ('YT', 'Yukon'),
    );
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_parking_lots')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='parking_lots')
    drivers = models.ManyToManyField(User, through='Reservation', related_name='reserved_parking_lots')
    street_type = models.CharField(max_length=4, choices=PROVINCE_CHOICES, default='BC')
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)
    province = models.CharField(max_length=255, choices=CHOICES_IN_STREET_TYPES, default='ST')
    city = models.CharField(max_length=255)
    image = models.URLField(max_length=255, null=True)
    phone = models.CharField(max_length=255)
    description = models.TextField(null=True)
    # reservation_any_time = ToggleField()
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    hourly_rate = models.CharField(max_length=255)

    def __str__(self):
        return self.phone
    # configurate starting_time, starting_date booth ending
    # def parking_past_midnight(self):
    #     return self.closing_time < self.opening_time

    def time_frame(self, date, starting_time, ending_time):
        reserved_parking = self.reservations.filter(date=date, starting_time=starting_time, ending_time=ending_time).aggregate(Sum('reserved_time'))
        reserved_parking = reserved_parking['reserved_time__sum'] or 0
        return (reserved_parking + starting_time) <= self.availability

class Reservation(models.Model):
    # for reservationes starting_date, ending_date, starting_time, ending_time, =total reservation time
    user = models.ForeignKey(User, related_name='reservations_made', on_delete=models.CASCADE)
    parking = models.ForeignKey(Parking, related_name='reservations', on_delete=models.CASCADE)
    # checkout_same_day = ToggleField()
    starting_date = models.DateField()
    ending_date = models.DateField()
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    total_time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return "{} {} - Total Time {}".format(self.date, self.time, self.reserved_time)

    def date_and_time(self):
        date = self.date.strftime("%Y-%m-%d")
        starting_time = self.starting_time.strftime("%H:%M")
        ending_time = self.ending_time.strftime("%H:%M")
        return "{} {} {}".format(date, starting_time, ending_time)
