from django.contrib import admin
from django.contrib import admin
from .models import FoodItem, Order, OrderItem

admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderItem)

