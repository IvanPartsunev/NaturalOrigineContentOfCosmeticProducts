from django.urls import path

from NaturalOriginContentOfCosmeticProducts.raw_materials.views import CreateRawMaterialView, UpdateRawMaterialView

urlpatterns = (
    path("create/", CreateRawMaterialView.as_view(), name="create_raw_material"),
    path("update/<int:pk>", UpdateRawMaterialView.as_view(), name="update_raw_material"),
)
