from django.contrib import admin
from .models import Host,EndUser,Vehicle

# Register your models here.
admin.site.register(Host)
admin.site.register(EndUser)
admin.site.register(Vehicle)