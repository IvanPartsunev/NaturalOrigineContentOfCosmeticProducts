from django.urls import path

from NaturalOriginContentOfCosmeticProducts.raw_materials.views import CreateRawMaterialView, UpdateRawMaterialView, \
    RawMaterialsView, DetailsRawMaterialView

urlpatterns = (
    path("", RawMaterialsView.as_view(), name="raw_materials"),
    path("<int:pk>/", DetailsRawMaterialView.as_view(), name="details_raw_material"),
    path("create/", CreateRawMaterialView.as_view(), name="create_raw_material"),
    path("update/<int:pk>", UpdateRawMaterialView.as_view(), name="update_raw_material"),
)
