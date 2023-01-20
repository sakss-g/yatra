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
    citizenship = models.ImageField(null = True, blank = True)

class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="enduser")
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10, null= True, blank=True)
    citizenship_id = models.CharField(max_length=20, null= True, blank=True)
    citizenship = models.ImageField(null = True, blank = True)
    license_no = models.CharField(max_length=20, null= True, blank=True)
    license = models.ImageField(null = True, blank = True)