from django.urls import path, include

from NaturalOriginContentOfCosmeticProducts.products.views import ProductCalculateNaturalContentView, \
    ProductCreateView, ProductDeleteView, ProductDetailsView, ProductListView, ProductFormulaCreateView, \
    ProductFormulaDetailView

urlpatterns = (
    path("", ProductListView.as_view(), name="product_list"),
    path("calculate/", ProductCalculateNaturalContentView.as_view(), name="product_calculate_noc"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("details/<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("formula/", include(
        [
            path("create/", ProductFormulaCreateView.as_view(), name="product_formula_create"),
            path("details/<int:pk>", ProductFormulaDetailView.as_view(), name="product_formula_details"),
        ],
    )),

)
