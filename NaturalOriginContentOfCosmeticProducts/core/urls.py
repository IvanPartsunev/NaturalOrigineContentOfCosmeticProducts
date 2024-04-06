from django.urls import path

from NaturalOriginContentOfCosmeticProducts.core.views import index, get_material_data_for_autofill, about

urlpatterns = (
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("autofill/", get_material_data_for_autofill, name="raw_material_autofill"),
)
