from django.contrib import admin
from .models import Userdata,Restaurant,Dish,Rating_dish,Rating_restaurant,Order

# Register your models here.
admin.site.register(Userdata)
admin.site.register(Rating_restaurant)
admin.site.register(Rating_dish)
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Order)
