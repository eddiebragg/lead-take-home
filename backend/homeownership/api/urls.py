from django.urls import path
from api import views

urlpatterns = [
    path("properties/<int:pk>/", views.PropertyDetailAPI.as_view()),
    path("payment/", views.PaymentAPI.as_view()),
]
