from django.contrib import admin
from api.models import Property, Payment


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["payment_date", "property", "amount"]
