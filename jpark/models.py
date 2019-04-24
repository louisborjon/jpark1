from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from mapbox import Geocoder

geocoder = Geocoder(access_token="sk.eyJ1Ijoidml0aHV5YW4iLCJhIjoiY2p1dWI0b2ZtMDVkeDN5bXF5dmR5NWlzNyJ9.XytADzlzPvLuSXPI5vroJw")


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    licence_plate = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255, null=True)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='CAD')


    def __str__(self):
        return self.full_name()

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def exists_for_user(self, user):
        return Profile.objects.filter(user_id=user.id).exists()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name, email=instance.email)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Category(models.Model):
    """ Category respresenting zone price """
    zone_in_category_choices = (
        ('5','zone_1'),
        ('3', 'zone_2'),
        ('1', 'zone_3'),
    );
    # we dont need this for now (April 17,2019)
    # zone_pricing = (
    #     ('zone_1', '5'),
    #     ('zone_2', '3'),
    #     ('zone_3', '1'),
    # );
    zone_price = MoneyField(choices=zone_in_category_choices, max_digits=14, decimal_places=2)
    # zone_price = models.IntegerField(choices=zone_pricing)


    def __str__(self):
        return "Your hourly rate will be {}.".format(self.zone_price)

    def location(self):
        return self.parking_lots.all()[0].hourly_rate

class Parking(models.Model):
    CHOICES_IN_STREET_TYPES = (
        ('Street', 'ST'),
        ('AVE', 'Avenue'),
        ('BLVD', 'Boulevard'),
        ('RD', 'Road'),
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
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='parking_lots')
    drivers = models.ManyToManyField(User, through='Reservation', related_name='reserved_parking_lots')
    street_type = models.CharField(max_length=4, choices=CHOICES_IN_STREET_TYPES, default='ST')
    street_name = models.CharField(max_length=255)
    street_number = models.IntegerField()
    zip_code = models.CharField(max_length=6)
    province = models.CharField(max_length=255, choices=PROVINCE_CHOICES, default='ON')
    city = models.CharField(max_length=255)
    image = models.URLField(max_length=255, null=True)
    phone = models.IntegerField()
    description = models.TextField(null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    hourly_rate = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()

    def full_address(self):
        return  f"{self.street_number} {self.street_name}, {self.city}, {self.zip_code}"

    def geo_from_address(self):
        response = geocoder.forward(self.full_address()).json()
        self.lat = response["features"][0]["center"][0]
        self.lng = response["features"][0]["center"][1]
        print(f"Updating Lat/Lng: {self.lat}, {self.lng}", file=sys.stderr)
        self.save()

    @receiver(post_save, sender=owner)
    def save_geo_cords(sender, instance, **kwargs):
        instance.geo_from_address()

    def __str__(self):
        return "Your parking spot is located at {} {} {}".format(self.street_number, self.street_name, self.street_type)
    # def parking_past_midnight(self):
    #     return self.closing_time < self.opening_time

    def time_frame(self, date, starting_time, ending_time):
        reserved_parking = self.reservations.filter(date=date, starting_time=starting_time, ending_time=ending_time).aggregate(Sum('reserved_time'))
        reserved_parking = reserved_parking['reserved_time__sum'] or 0 #trying to not allow two reservations overlapping
        return (reserved_parking + starting_time) <= self.availability

class Reservation(models.Model):
    # for reservationes starting_date, ending_date, starting_time, ending_time, =total reservation time
    Profile = models.ForeignKey(User, related_name='reservations_made', on_delete=models.CASCADE)
    parking = models.ForeignKey(Parking, related_name='reservations', on_delete=models.CASCADE)
    # checkout_same_day = ToggleField()
    starting_date = models.DateField()
    ending_date = models.DateField()
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)


    #def __str__(self):
        #return "Your reservation is on {}".format(self.total_time).hour

        #return "Your remaining balance will be {}".format(self.user.profile.balance -(self.ending_time - self.starting_time) * self.parking.category.zone_price)


    def date_and_time(self):
        date = self.date.strftime("%Y-%m-%d")
        starting_time = self.starting_time.strftime("%H:%M")
        ending_time = self.ending_time.strftime("%H:%M")
        return "{} {} {}".format(date, starting_time, ending_time)
