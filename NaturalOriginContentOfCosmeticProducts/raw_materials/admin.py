from django.contrib import admin

from NaturalOriginContentOfCosmeticProducts.core.mixins import FormatAdminDate
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


@admin.register(RawMaterial)
class RawMaterialAdmin(FormatAdminDate, admin.ModelAdmin):
    list_display = (
        "trade_name",
        "inci_name",
        "material_type",
        "natural_origin_content",
        "is_deleted",
        "formatted_edited_on",
        "formatted_created_on",
    )

    search_fields = (
        "trade_name",
        "inci_name",
    )

    ordering = (
        "trade_name",
    )

