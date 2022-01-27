from atexit import register

from django.contrib import admin

from .models import Dish, OrderTime, Order, TypeFood

register = admin.site.register

register(Dish)
register(Order)
register(OrderTime)
register(TypeFood)
