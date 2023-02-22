from django.contrib import admin
from .models import (Item, Category, Order, Comment)

# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Comment)
