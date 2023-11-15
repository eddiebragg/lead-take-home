from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Property(models.Model):
    flat_name = models.CharField(max_length=100, null=True, blank=True)
    building_name = models.CharField(max_length=100, null=True, blank=True)
    building_number = models.CharField(max_length=10, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=8, null=True, blank=True)
    purchase_date = models.DateField()
    purchase_price = models.IntegerField(default=0)
    deposit = models.IntegerField(default=0)

    @property
    def full_address(self) -> str:

        return ", ".join(
            [
                value
                for value in [
                    self.flat_name,
                    self.building_number,
                    self.building_name,
                    self.street,
                    self.town,
                    self.city,
                    self.county,
                    self.postcode,
                ]
                if value
            ]
        )

    @property
    def staircasing_amount(self) -> int:
        return (self.purchase_price / 100) * settings.ANNUAL_STAIRCASING_PERCENTAGE

    @property
    def total_amount_paid(self) -> int:
        return sum(self.payments.values_list("amount", flat=True)) + self.deposit

    def __str__(self):
        return self.full_address


class Payment(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(settings.MINIMUM_PAYMENT_AMOUNT)]
    )
    payment_date = models.DateField(auto_created=True)
