from django.urls import path

from NaturalOriginContentOfCosmeticProducts.core.views import index, get_material_data_for_autofill

urlpatterns = (
    path("", index, name="index"),
    path("autofill/", get_material_data_for_autofill, name="raw_material_autofill"),
)
