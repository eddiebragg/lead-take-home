from datetime import date

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request

from api.models import Property
from api.serializers import PropertySerializer, PaymentSerializer


class PropertyDetailAPI(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)


class PaymentAPI(generics.CreateAPIView):

    serializer_class = PaymentSerializer

    def perform_create(self, serializer: PaymentSerializer):
        serializer.save(payment_date=date.today())
