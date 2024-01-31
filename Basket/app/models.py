from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Userdata(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    S="seller"
    U="user"
    User_types=[
       (S,"Seller"),
       (U,"User"),
    ]
    seller_or_user=models.CharField(max_length=30,choices=User_types)
    email=models.EmailField(max_length=300)
class Restaurant(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
    address=models.CharField(max_length=100)
    rating_restaurant=models.ManyToManyField(User, through='Rating_restaurant',related_name='user_ratings_for_restaurant')

class Dish(models.Model):
    seller = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    new_order_by= models.ManyToManyField(User, through='Order',related_name="order")
    rating_dish=models.ManyToManyField(User, through='Rating_dish',related_name="dish_rating")

    def is_past_order(self, user):
        order = Order.objects.filter(dish=self, user=user).first()
        if order and order.order_time:
            return timezone.now() > order.order_time + timezone.timedelta(hours=1)
        return False

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    order_time = models.DateTimeField(null=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    seller=models.ForeignKey(Restaurant,on_delete=models.CASCADE,null=True)

    class Meta:
        unique_together = ('user', 'dish')
        
    
class Basket(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    order_time=models.DateTimeField(null=True)
    seller=models.OneToOneField(Restaurant,on_delete=models.CASCADE,null=True)

    
class Wallet(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)    
    balance=models.IntegerField(default=2000)



    



          
class Rating_dish(models.Model):

    dish=models.ForeignKey(Dish, on_delete=models.CASCADE,related_name="dish_rating")
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    one=1
    two=2
    three=3
    four=4
    five=5
    rate=[
        (one,"1"),
        (two,"2"),
        (three,"3"),
        (four,"4"),
        (five,"5"),
    ]
    ratings= models.IntegerField(choices=rate)
    description=models.CharField(max_length=300,blank=True)

class Rating_restaurant(models.Model):

    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="restaurant_user_ratings")
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='user_restaurant_ratings')
    one=1
    two=2
    three=3
    four=4
    five=5
    rate=[
        (one,"1"),
        (two,"2"),
        (three,"3"),
        (four,"4"),
        (five,"5"),
    ]
    ratings= models.IntegerField(choices=rate)
    description=models.CharField(max_length=300,blank=True)    



