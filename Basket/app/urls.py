from django.urls import path,include
from app import views
from .views import index


urlpatterns = [
    path("", views.index),
    path("logout/",views.logout_user,name="logout"),
    path("profile/",views.profile,name="profile"),
    path("seller_inteface/",views.seller_interface,name="seller_interface"),
    path("user_interface/",views.user_interface,name="user_interface"),
    path("index/",views.index,name="index"),
    path("add_dish/",views.add_dish,name="add_dish"),
    path("view_bookings/",views.view_bookings,name="view_bookings"),
    path("menu/",views.Menu,name="menu"),
    path("search/",views.search,name="search"),
    path("place_order/<int:dish_id>/",views.place_order,name="place_order"),
    path("wallet/",views.wallet,name="wallet"),
    path("wallet/add_money/",views.add_money,name="add_money"),
    path("view_myorders/",views.view_my_orders,name="view_myorders"),
    path("add_to_basket/<int:dish_id>",views.add_to_basket,name="add_to_basket"),
    path("show_basket/",views.show_basket,name="show_basket"),
    path("rate_dish/<int:dish_id>",views.rate_dish,name="rate_dish"),
    path("rate_restaurant/<int:dish_id>",views.rate_restaurant,name="rate_restaurant"),
    path("view_ratings/",views.view_ratings,name="view_ratings"),

]