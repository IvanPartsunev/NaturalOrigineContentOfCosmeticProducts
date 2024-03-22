from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    path("admin/", admin.site.urls),
    path("", include("NaturalOriginContentOfCosmeticProducts.core.urls")),
    path("raw-materials/", include("NaturalOriginContentOfCosmeticProducts.raw_materials.urls")),
    path("product/", include("NaturalOriginContentOfCosmeticProducts.products.urls")),
    path("accounts/", include("NaturalOriginContentOfCosmeticProducts.accounts.urls")),
)
