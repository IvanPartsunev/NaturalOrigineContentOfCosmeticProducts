from django.urls import path

from NaturalOriginContentOfCosmeticProducts.raw_materials.views import RawMaterialCreateView, RawMaterialUpdateView, \
    RawMaterialListView, RawMaterialDetailsView

urlpatterns = (
    path("", RawMaterialListView.as_view(), name="raw_materials"),
    path("<int:pk>/", RawMaterialDetailsView.as_view(), name="details_raw_material"),
    path("create/", RawMaterialCreateView.as_view(), name="create_raw_material"),
    path("update/<int:pk>", RawMaterialUpdateView.as_view(), name="update_raw_material"),
)

