from django.urls import path, include

from NaturalOriginContentOfCosmeticProducts.products.views import ProductCalculateNaturalContentView, \
    ProductCreateView, ProductDeleteView, ProductDetailsView, ProductListView, ProductFormulaCreateView, \
    ProductFormulaDetailView, ProductUpdateView, ProductFormulaDeleteView, ProductFormulaUpdateView

urlpatterns = (
    path("list/", ProductListView.as_view(), name="product_list"),
    path("calculate/", ProductCalculateNaturalContentView.as_view(), name="product_calculate_noc"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/details/", ProductDetailsView.as_view(), name="product_details"),
    path("<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("formula/", include(
        [
            path("create/", ProductFormulaCreateView.as_view(), name="product_formula_create"),
            path("<int:pk>/details/", ProductFormulaDetailView.as_view(), name="product_formula_details"),
            path("<int:pk>/update/", ProductFormulaUpdateView.as_view(), name="product_formula_update"),
            path("<int:pk>/delete/", ProductFormulaDeleteView.as_view(), name="product_formula_delete"),
        ],
    )),

)
