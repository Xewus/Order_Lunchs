from atexit import register

from django.contrib import admin

from .models import Dish, OrderTime, Order, TypeFood, DeliveryDate

register = admin.site.register

register(DeliveryDate)
register(Dish)
register(Order)
register(OrderTime)
register(TypeFood)
