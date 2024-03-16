from django.urls import path

from NaturalOriginContentOfCosmeticProducts.calculate_noi.views import CalculateNaturalOriginContentView

urlpatterns = (
    path("", CalculateNaturalOriginContentView.as_view(), name="calculate_noi"),
)
