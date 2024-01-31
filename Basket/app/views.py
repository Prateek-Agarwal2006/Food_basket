from django.utils import timezone
from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login,logout
from django.http import HttpResponse
from .forms import registrationform,Restaurantform,add_dishform,add_moneyform,rating_dish_form,rating_restaurant_form
from .models import Userdata,Restaurant,Dish,Wallet,Basket,Rating_dish,Rating_restaurant,Order
from fuzzywuzzy import fuzz
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,"index.html",)

def logout_user(request):
    logout(request)
    return redirect("index")

def profile(request):
    try:
        user_data=Userdata.objects.get(user=request.user)
        user_type=user_data.seller_or_user
        if user_type=="seller":

            return redirect("seller_interface")
        else :
            wallet,created=Wallet.objects.get_or_create(user=request.user,defaults={'balance':2000})
            wallet.save()
            return redirect("user_interface")
    except Userdata.DoesNotExist:

      if request.method == "POST":
        form = registrationform(request.POST)

        if form.is_valid():
            user_type = form.cleaned_data.get('seller_or_user')
            user = request.user
            email = user.email

            
            userdata, created = Userdata.objects.get_or_create(user=user, defaults={'email': email})

            userdata.seller_or_user = user_type
            userdata.save()

            if user_type == 'seller':
                return redirect("seller_interface")
            else:
                wallet,created=Wallet.objects.get_or_create(user=request.user,defaults={'balance':2000})
                wallet.save()
                return redirect("user_interface")

      else:
        form = registrationform()

      return render(request, "profile.html", {'form': form})
    
def user_interface(request):
    if request.user.is_anonymous:
        return redirect("login/")
    return render(request,'user_interface.html',)


def seller_interface(request):
    if request.user.is_anonymous:
        return redirect("login/")
    
    user_data = Userdata.objects.get(user=request.user)
    if user_data.seller_or_user != "seller":
        login_url = reverse('account_login')  
        message = "You are not authorized. Please <a href='{}'>login</a>.".format(login_url)
        return HttpResponse(message, content_type="text/html")

    name = address = None  

    try:
        my_restaurant = Restaurant.objects.get(owner=request.user)
        name = my_restaurant.name
        address = my_restaurant.address
    except Restaurant.DoesNotExist:
        if request.method == "POST":
            form = Restaurantform(request.POST)
            if form.is_valid():
                new_restaurant = form.save(commit=False)
                new_restaurant.owner = request.user
                new_restaurant.save()
                name = new_restaurant.name
                address = new_restaurant.address
            else:
                return render(request, "restaurant_details.html", {"form": form})
        else:
            form = Restaurantform()
            return render(request, "restaurant_details.html", {"form": form})

    return render(request, "seller_interface.html", {"name": name, "address": address})


def index(request):
    return render(request,"index.html",)
@login_required
def add_dish(request):
    who=Userdata.objects.get(user=request.user)
    if who.seller_or_user!='seller':
        login_url = reverse('account_login')  
        message = "You are not authorized. Please <a href='{}'>login</a>.".format(login_url)
        return HttpResponse(message, content_type="text/html")
    if request.method!="POST":
        form=add_dishform()
        return render(request,"add_dish.html",{'form':form})
    elif request.method=="POST":
        form=add_dishform(request.POST)
        form.save(commit=False)
        name=form.cleaned_data.get("name")
        price=form.cleaned_data.get("price")
        #form.save()
        restaurant=Restaurant.objects.get(owner=request.user)
        new_dish=Dish.objects.create(seller=restaurant,name=name,price=price)
        new_dish.save()

    return redirect("menu")

@login_required
def Menu(request):
    who=Userdata.objects.get(user=request.user)
    if who.seller_or_user!='seller':
        login_url = reverse('account_login')  
        message = "You are not authorized. Please <a href='{}'>login</a>.".format(login_url)
        return HttpResponse(message, content_type="text/html")
    restaurant=Restaurant.objects.get(owner=request.user)
    dishes=Dish.objects.filter(seller=restaurant)
    return render(request,"menu.html",{'dishes':dishes})
@login_required
def view_bookings(request):
    who=Userdata.objects.get(user=request.user)
    if who.seller_or_user!='seller':
        login_url = reverse('account_login')  
        message = "You are not authorized. Please <a href='{}'>login</a>.".format(login_url)
        return HttpResponse(message, content_type="text/html")
    pending_orders=[]
    past_orders=[]
    restaurant=Restaurant.objects.get(owner=request.user)
    order=Order.objects.filter(seller=restaurant)
    
    for dish in order:
        if timezone.now() >dish.order_time + timezone.timedelta(hours=1):
            past_orders.append(dish)
        else:
            pending_orders.append(dish)
    return render(request,"view_bookings.html",{"past_orders":past_orders,"pending_orders":pending_orders})            







def search(request):
    if request.method == "GET":
        name = request.GET.get('dish_name', '')
        
        all_dishes =Dish.objects.all()
        


        matched_dishes = []
        for dish in all_dishes:
            

            similarity = fuzz.ratio(dish.name.lower(), name.lower())
            
            if similarity > 70 :
                matched_dishes.append(dish)

        return render(request, "search.html", {'dishes': matched_dishes})
@login_required
def add_to_basket(request,dish_id):
    dish_data=Dish.objects.get(id=dish_id)
    basket,created=Basket.objects.get_or_create(user=request.user,name=dish_data.name,price=dish_data.price,seller=dish_data.seller)
    basket.save()
    return redirect("show_basket")
@login_required
def show_basket(request):    
    whole_basket=Basket.objects.filter(user=request.user)
    return render(request,"basket.html",{"whole_basket":whole_basket})
@login_required
def place_order(request,dish_id):
    basket=Basket.objects.get(id=dish_id)
    #print(basket,basket.name,basket.price,basket.user)
    dish_data=Dish.objects.get(name=basket.name,price=basket.price,seller=basket.seller)
    user_wallet=Wallet.objects.get(user=request.user)
    
    if user_wallet.balance>=dish_data.price:
        dish_data.new_order_by.add(request.user)
        dish_data.save()
        try:
            order = Order.objects.create(user=request.user, dish=dish_data, order_time=timezone.now(),name=dish_data.name,price=dish_data.price,seller=dish_data.seller)
            order.save()
        except IntegrityError :
            order=Order.objects.get(user=request.user,dish=dish_data)
            order.price=dish_data.price
            order.name=dish_data.name
            order.order_time=timezone.now()
            order.seller=dish_data.seller
            order.save()  
        user_wallet.balance=user_wallet.balance-dish_data.price
        user_wallet.save()
        basket=Basket.objects.get(id=dish_id)
        basket.delete()
        #print(order.order_time)

        return redirect("view_myorders")
    else:
        return HttpResponse("Not enough money, pls add more money.",)
    
@login_required
def wallet(request):
    user_wallet,created=Wallet.objects.get_or_create(user=request.user,defaults={'balance':2000})
    balance=user_wallet.balance
    return render(request,"wallet.html",{"balance":balance})
@login_required
def add_money(request):
    if request.method!="POST":
        form=add_moneyform()
        return render(request,"add_money.html",{"form":form})
    elif request.method=="POST":
        form=add_moneyform(request.POST)
        if form.is_valid():
            
            amount=form.cleaned_data.get("add_amount")
            user_wallet,created=Wallet.objects.get_or_create(user=request.user,defaults={'balance':2000})
            user_wallet.balance+=amount
            user_wallet.save()
            return redirect("wallet")
        
    return render(request,"add_money.html",{"form":form})   
@login_required
def view_my_orders(request):
    my_orders=Order.objects.filter(user=request.user)
    past_orders=[]
    pending_orders=[]
    for order in my_orders:
        dish = order.dish
        if timezone.now() > order.order_time + timezone.timedelta(hours=1):
            dish_rating = Rating_dish.objects.filter(dish=dish, user=request.user).first()
            restaurant_rating = Rating_restaurant.objects.filter(restaurant=dish.seller, user=request.user).first()
            order.dish_rating = dish_rating  # not is database just generate it now and show
            order.restaurant_rating = restaurant_rating
            past_orders.append(order)
        else:
            pending_orders.append(order)

    return render(request, "view_myorders.html", {"past_orders": past_orders, "pending_orders": pending_orders})
@login_required
def rate_dish(request,dish_id):
    if request.method!="POST":
        form=rating_dish_form()
        return render(request,"rating.html",{"form":form})
    elif request.method=="POST":
        form=rating_dish_form(request.POST)
        form.save( commit=False)
        rating=form.cleaned_data.get("ratings")
        description=form.cleaned_data.get("description")
        print("Received dish_id:", dish_id)
        dish=Dish.objects.get(id=dish_id) # problematic 
        rate_data,created=Rating_dish.objects.get_or_create(user=request.user,dish=dish,ratings=rating,description=description)
        rate_data.save()
        return redirect("view_myorders")
@login_required    
def rate_restaurant(request,dish_id):
    if request.method!="POST":
        form=rating_restaurant_form()
        return render(request,"rating.html",{"form":form})
    elif request.method=="POST":
        form=rating_restaurant_form(request.POST)
        form.save(commit=False)
        rating=form.cleaned_data.get("ratings")
        description=form.cleaned_data.get("description")
        dish=Dish.objects.get(id=dish_id)
        restaurant=dish.seller
        rate_data,created=Rating_restaurant.objects.get_or_create(user=request.user,restaurant=restaurant,ratings=rating,description=description)
        rate_data.save()
        return redirect("view_myorders")
    
@login_required    
def view_ratings(request):
    who=Userdata.objects.get(user=request.user)
    if who.seller_or_user!='seller':
        login_url = reverse('account_login')  
        message = "You are not authorized. Please <a href='{}'>login</a>.".format(login_url)
        return HttpResponse(message, content_type="text/html")
    restaurant=Restaurant.objects.get(owner=request.user)
    ratings=Rating_restaurant.objects.filter(restaurant=restaurant)
    return render(request,"view_ratings.html",{"ratings":ratings})

    

    