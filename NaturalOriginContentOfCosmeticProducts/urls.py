from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    path("admin/", admin.site.urls),
    path("raw-materials/", include("NaturalOriginContentOfCosmeticProducts.raw_materials.urls")),
)
