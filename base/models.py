from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="host")
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, null= True, blank=True)
    address = models.CharField(max_length=100, null= True, blank=True)
    citizenship_id = models.CharField(max_length=20, null= True, blank=True)
    citizenship = models.ImageField(upload_to='host/profile', null = True, blank = True)
    pic = models.ImageField(upload_to='host/profile', default='default_profile.jpg')
    is_approved = models.BooleanField(default=False)

class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="enduser")
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, null= True, blank=True)
    citizenship_id = models.CharField(max_length=20, null= True, blank=True)
    citizenship = models.ImageField(upload_to='enduser/profile', null = True, blank = True)
    license_no = models.CharField(max_length=20, null= True, blank=True)
    license = models.ImageField(upload_to='enduser/profile', null = True, blank = True)
    pic = models.ImageField(upload_to='enduser/profile', default='default_profile.jpg')
    is_approved = models.BooleanField(default=False)

class Location(models.Model):
    name=models.CharField(max_length=25)

class Vehicle(models.Model):
    types = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Jeep', 'Jeep'),
        ('Mini-Van', 'Mini-Van'),
        ('Other', 'Other'),
    )
    number_plate = models.CharField(max_length=20, unique=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="owner")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name="place")
    bluebook = models.ImageField(upload_to="host/vehicle")
    bluebook_id = models.CharField(max_length=25)
    image1 = models.ImageField(upload_to="host/vehicle")
    image2 = models.ImageField(upload_to="host/vehicle")
    image3 = models.ImageField(upload_to="host/vehicle", null=True, blank=True)
    description = models.CharField(max_length=2000)
    feature = models.CharField(max_length=1000)
    price = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=types)


class Travelogue(models.Model):
    enduser = models.ForeignKey(EndUser, on_delete=models.CASCADE, related_name="blogger")
    description = models.CharField(max_length=10000)
    image1 = models.ImageField(upload_to="enduser/travelogue")
    image2 = models.ImageField(upload_to="enduser/travelogue", null=True, blank=True)