from django.urls import path

from NaturalOriginContentOfCosmeticProducts.raw_materials.views import RawMaterialCreateView, RawMaterialUpdateView, \
    RawMaterialListView, RawMaterialDetailsView

urlpatterns = (
    path("", RawMaterialListView.as_view(), name="raw_material_list"),
    path("<int:pk>/", RawMaterialDetailsView.as_view(), name="raw_material_details"),
    path("create/", RawMaterialCreateView.as_view(), name="raw_material_create"),
    path("update/<int:pk>", RawMaterialUpdateView.as_view(), name="raw_material_update"),
)

