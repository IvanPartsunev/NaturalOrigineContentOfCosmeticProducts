from django.urls import path

from NaturalOriginContentOfCosmeticProducts.calculate_noi.views import CalculateNaturalContentView

urlpatterns = (
    path("", CalculateNaturalContentView.as_view(), name="calculate_noi"),
)
