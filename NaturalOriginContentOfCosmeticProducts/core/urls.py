from django.urls import path

from NaturalOriginContentOfCosmeticProducts.core.views import index

urlpatterns = (
    path("", index, name="index"),
)
