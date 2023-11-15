from datetime import date

from django.test import TestCase
from freezegun import freeze_time
from rest_framework.test import APIClient

from api.models import Property, Payment


class TestPropertyDetailAPI(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_object_does_not_exist(self) -> None:
        response = self.client.get("/api/properties/34/")
        self.assertEquals(response.status_code, 404)

    def test_get_object(self) -> None:
        property = Property.objects.create(
            purchase_date=date.today(),
            purchase_price=250_000,
            deposit=12500,
            building_name="Test Building",
            street="street 1",
            postcode="BS20 8JG",
        )
        response = self.client.get(f"/api/properties/{property.id}/")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "full_address": "Test Building, street 1, BS20 8JG",
                "purchase_price": 250_000,
                "total_amount_paid": 12500,
            },
        )


class TestPaymentAPI(TestCase):
    @freeze_time("2023-01-01")
    def setUp(self) -> None:
        self.client = APIClient()
        self.property = Property.objects.create(
            purchase_date=date.today(), purchase_price=250_000, deposit=12500
        )

    def test_bad_request_no_data(self) -> None:
        response = self.client.post("/api/payment/", {}, format="json")
        self.assertEquals(response.status_code, 400)

        data = response.data

        self.assertEquals(data["amount"][0], "This field is required.")
        self.assertEquals(data["property"][0], "This field is required.")

    def test_bad_request_empty_data(self) -> None:
        response = self.client.post(
            "/api/payment/", {"amount": "", "property": ""}, format="json"
        )
        self.assertEquals(response.status_code, 400)

        data = response.data

        self.assertEquals(data["amount"][0], "A valid integer is required.")
        self.assertEquals(data["property"][0], "This field may not be null.")

    def test_bad_request_property_does_not_exist(self) -> None:
        response = self.client.post(
            "/api/payment/", {"amount": 60, "property": 999}, format="json"
        )
        self.assertEquals(response.status_code, 400)

        data = response.data

        self.assertEquals(
            data["property"][0], 'Invalid pk "999" - object does not exist.'
        )

    def test_bad_request_below_minimum_amount(self) -> None:
        response = self.client.post(
            "/api/payment/", {"amount": 49, "property": self.property.id}
        )

        self.assertEquals(response.status_code, 400)

        data = response.data

        self.assertEquals(
            data["amount"][0], "Ensure this value is greater than or equal to 50."
        )

    @freeze_time("2023-11-14")
    def test_payment_date(self) -> None:
        self.client.post("/api/payment/", {"amount": 51, "property": self.property.id})
        payment = Payment.objects.get(property=self.property)
        self.assertEquals(payment.payment_date.strftime("%Y-%m-%d"), "2023-11-14")


class TestPaymentAPIStairCasing(TestCase):
    @freeze_time("2020-12-31")
    def setUp(self) -> None:
        self.client = APIClient()
        self.property = Property.objects.create(
            purchase_date=date.today(), purchase_price=250_000, deposit=12500
        )

    @freeze_time("2021-01-01")
    def test_one_off_payment_over(self) -> None:
        response = self.client.post(
            "/api/payment/", {"amount": 12501, "property": self.property.id}
        )

        self.assertEquals(response.status_code, 400)
        data = response.data

        self.assertEquals(
            data["non_field_errors"][0],
            "The amount takes you above the maximum annual payment.",
        )

    @freeze_time("2021-01-01")
    def test_paying_over_purchase_price(self):
        response = self.client.post(
            "/api/payment/", {"amount": 250_001, "property": self.property.id}
        )

        self.assertEquals(response.status_code, 400)
        data = response.data

        self.assertEquals(
            data["non_field_errors"][0],
            "The amount takes you above the purchase price.",
        )

    def test_payment_over_time(self) -> None:
        with freeze_time("2022-01-01"):
            response = self.client.post(
                "/api/payment/", {"amount": 12500, "property": self.property.id}
            )

            self.assertEquals(response.status_code, 201)

        with freeze_time("2022-02-01"):
            response = self.client.post(
                "/api/payment/", {"amount": 51, "property": self.property.id}
            )

            self.assertEquals(response.status_code, 400)

            data = response.data

            self.assertEquals(
                data["non_field_errors"][0],
                "The amount takes you above the maximum annual payment.",
            )

        with freeze_time("2023-01-01"):
            response = self.client.post(
                "/api/payment/", {"amount": 12500, "property": self.property.id}
            )

            self.assertEquals(response.status_code, 201)
