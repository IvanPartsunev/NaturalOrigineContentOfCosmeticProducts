from django.contrib import admin

from NaturalOriginContentOfCosmeticProducts.core.mixins import FormatAdminDate
from NaturalOriginContentOfCosmeticProducts.products.models import Product, ProductFormula, ProductFormulaRawMaterial


@admin.register(Product)
class ProductAdmin(FormatAdminDate, admin.ModelAdmin):
    list_display = (
        "product_name",
        "owner",
        "formatted_edited_on",
        "formatted_created_on",
    )

    search_fields = (
        "product_name",
        "owner",
    )

    ordering = (
        "product_name",
        "owner",
    )


@admin.register(ProductFormula)
class ProductFormulaAdmin(FormatAdminDate, admin.ModelAdmin):
    list_display = (
        "product",
        "description",
        "owner",
        "formatted_edited_on",
        "formatted_created_on",
    )

    search_fields = (
        "product",
    )

    ordering = (
        "product",
        "owner",
        "edited_on",
    )


@admin.register(ProductFormulaRawMaterial)
class ProductFormulaRawMaterialAdmin(FormatAdminDate, admin.ModelAdmin):
    list_display = (
        "formula",
        "raw_material",
        "raw_material_content",
        "formatted_edited_on",
        "formatted_created_on",
    )

    search_fields = (
        "formula",
    )

    ordering = (
        "formula",
    )
