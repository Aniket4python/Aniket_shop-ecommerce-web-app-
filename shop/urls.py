from django.contrib import admin
from django.urls import path
from .views import*

urlpatterns = [
    path('', home, name="home" ),
    path('signup', signup, name="signup" ),
    path('login_page', login_page, name="login_page" ),
    path('logout', logout, name="logout" ),
    path('cart', cart, name="cart" ),
    path('checkout', checkout, name="checkout" ),
    path('order', order_page, name="order" ),

]