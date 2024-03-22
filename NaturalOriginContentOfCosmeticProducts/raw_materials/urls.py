from django.urls import path

from NaturalOriginContentOfCosmeticProducts.raw_materials.views import RawMaterialCreateView, RawMaterialUpdateView, \
    RawMaterialListView, RawMaterialDetailsView, RawMaterialDeleteView

urlpatterns = (
    path("list/", RawMaterialListView.as_view(), name="raw_material_list"),
    path("create/", RawMaterialCreateView.as_view(), name="raw_material_create"),
    path("<int:pk>/", RawMaterialDetailsView.as_view(), name="raw_material_details"),
    path("<int:pk>/update/", RawMaterialUpdateView.as_view(), name="raw_material_update"),
    path("<int:pk>/delete/", RawMaterialDeleteView.as_view(), name="raw_material_delete"),
)
