from django.contrib import admin
from django.urls import path
from home import views
from home.views import *

from django.conf.urls.static import static




urlpatterns = [
    path("",        views.homepage, name='home'),
    path("contact", views.contact,  name='contact'),
    path('register', views.register_page, name="register"),
    path('login', views.login_page, name="login_page"),
    path('logout', views.logout_page, name="logout"),
    path('process_order/', views.processOrder, name="process_order"),
    path("buyer",  views.buyer,   name='buyer'),
    path("cart",    views.cart,     name='cart'), 
    path("search",  views.search,   name='search'),
    path('update_item/', views.update_item, name='update_item'),
    path("checkout",views.checkout, name='checkout'),
    path("seller",views.seller, name='seller'),

]

