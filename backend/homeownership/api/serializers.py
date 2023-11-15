from datetime import date

from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from api.models import Property, Payment


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["full_address", "purchase_price", "total_amount_paid"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["amount", "property"]

    def validate(self, attrs):
        """
        Check the amount is not going over the staircasing for the year
        """
        property = attrs["property"]
        amount = attrs["amount"]
        today = date.today()

        start_date = property.purchase_date.replace(year=today.year)
        if start_date > today:
            start_date = start_date - relativedelta(years=1)

        end_date = start_date + relativedelta(years=1)

        payments = property.payments.all()

        total_paid = (
            sum([payment.amount for payment in payments]) + amount + property.deposit
        )

        if total_paid > property.purchase_price:
            raise serializers.ValidationError(
                "The amount takes you above the purchase price."
            )

        annual_payment_amount = sum(
            [
                payment.amount
                for payment in payments
                if payment.payment_date >= start_date
                and payment.payment_date < end_date
            ]
        )

        if (annual_payment_amount + amount) > property.staircasing_amount:
            raise serializers.ValidationError(
                "The amount takes you above the maximum annual payment."
            )

        return attrs
