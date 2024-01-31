from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Userdata,Restaurant,Dish,Rating_dish,Rating_restaurant

class registrationform(ModelForm):
    class Meta:
        model=Userdata
        exclude=("user","email")

class Restaurantform(ModelForm):
    class Meta:
        model=Restaurant
        exclude=("owner","rating_restaurant")

class add_dishform(ModelForm):
    class Meta:
        model=Dish
        exclude=("seller","order_time","new_order_by","rating_dish")

class add_moneyform(forms.Form):
    add_amount=forms.IntegerField()  

class rating_dish_form(ModelForm):
    class Meta:
        model=Rating_dish
        exclude=("user","restaurant","dish",)   
class rating_restaurant_form(ModelForm):
    class Meta:
        model=Rating_dish
        exclude=("user","restaurant","dish",)          