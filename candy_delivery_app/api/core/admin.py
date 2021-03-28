from django.contrib import admin
from .models import Courier, Order


class CourierAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(Courier, CourierAdmin)
admin.site.register(Order, OrderAdmin)