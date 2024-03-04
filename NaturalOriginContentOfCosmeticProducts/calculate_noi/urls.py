from django.urls import path

from NaturalOriginContentOfCosmeticProducts.calculate_noi.views import CalculateNaturalOriginContent

urlpatterns = (
    path("", CalculateNaturalOriginContent.as_view(), name="calculate_noi"),
)
