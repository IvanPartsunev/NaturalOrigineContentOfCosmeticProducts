from django.urls import path

from NaturalOriginContentOfCosmeticProducts.calculate_noi.views import CalculateNaturalContentView, \
    get_material_data_for_autofill

urlpatterns = (
    path("", CalculateNaturalContentView.as_view(), name="calculate_noi"),
    path("autofill/", get_material_data_for_autofill, name="raw_material_autofill"),
)
