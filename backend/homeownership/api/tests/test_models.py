from datetime import date

from django.test import TestCase

from api.models import Property


class TestPropertyModel(TestCase):
    def test_full_address(self) -> None:
        property = Property.objects.create(purchase_date=date.today())
        self.assertEquals(property.full_address, "")

        property.flat_name = "Flat 1"
        property.building_number = "12"
        property.building_name = "Test Building"
        property.street = "street 1"
        property.town = "Hounslow"
        property.city = "London"
        property.county = "County"
        property.postcode = "EX18 7SN"
        property.save()

        self.assertEquals(
            property.full_address,
            "Flat 1, 12, Test Building, street 1, Hounslow, London, County, EX18 7SN",
        )

    def test_staircasing_amount(self):
        property = Property.objects.create(
            purchase_date=date.today(), purchase_price=250000
        )
        self.assertEquals(property.staircasing_amount, 12500)
