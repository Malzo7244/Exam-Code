from django.contrib import admin
from .models import Pizza, Order, PizzaOption

admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(PizzaOption)
