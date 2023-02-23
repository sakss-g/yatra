from django.contrib import admin
from .models import Host, EndUser, Vehicle, Rents, Travelogue

# Register your models here.
admin.site.register(Host)
admin.site.register(EndUser)
admin.site.register(Vehicle)
admin.site.register(Rents)
admin.site.register(Travelogue)