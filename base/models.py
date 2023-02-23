from django.db import models
from django.contrib.auth.models import User
from pathlib import Path

status = (
        ('Approved', 'Approved'),
        ('Rejected','Rejected'),
        ('Pending','Pending'),
    )

# Create your models here.
class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="host")
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, null= True, blank=True)
    address = models.CharField(max_length=100, null= True, blank=True)
    citizenship_id = models.CharField(max_length=20, null= True, blank=True)
    citizenship = models.ImageField(upload_to='host/profile', default='default_photo.jpg')
    pic = models.ImageField(upload_to='host/profile', default='default_profile.jpg')
    is_approved = models.CharField(max_length=10, choices=status, default="Pending")


class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="enduser")
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, null= True, blank=True)
    citizenship_id = models.CharField(max_length=20, null= True, blank=True)
    citizenship = models.ImageField(upload_to='enduser/profile',  default='default_photo.jpg')
    license_no = models.CharField(max_length=20, null= True, blank=True)
    license = models.ImageField(upload_to='enduser/profile',  default='default_photo.jpg')
    pic = models.ImageField(upload_to='enduser/profile', default='default_profile.jpg')
    is_approved = models.CharField(max_length=10, choices=status, default="Pending")


class Location(models.Model):
    name=models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name

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
    description = models.TextField(max_length=2000)
    feature = models.TextField(max_length=1000)
    price = models.PositiveIntegerField() 
    type = models.CharField(max_length=10, choices=types)
    is_approved = models.CharField(max_length=10, choices=status, default="Pending")
    is_rented = models.BooleanField(default=False)

class Rents(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    renter = models.ForeignKey(EndUser, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Travelogue(models.Model):
    enduser = models.ForeignKey(EndUser, on_delete=models.CASCADE, related_name="blogger")
    description = models.CharField(max_length=10000)
    image1 = models.ImageField(upload_to="enduser/travelogue")
    image2 = models.ImageField(upload_to="enduser/travelogue", null=True, blank=True)
    is_approved = models.CharField(max_length=10, choices=status, default="Pending")

