from django.contrib import admin

from .models import Product, Item


admin.site.register(Product)
admin.site.register(Item)