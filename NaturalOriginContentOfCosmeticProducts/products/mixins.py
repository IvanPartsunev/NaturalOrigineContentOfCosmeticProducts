from django.contrib.auth import mixins as auth_mixins
from django.core import exceptions
from django.shortcuts import get_object_or_404
from django.utils import timezone

from NaturalOriginContentOfCosmeticProducts.products.models import Product, ProductFormula, \
    ProductFormulaRawMaterial
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class CalculateSaveMixin:
    MINIMUM_SUM_OF_CONTENT = 100
    MAXIMUM_SUM_OF_CONTENT = 103
    CALCULATION_ERROR_MESSAGE = "Sum of raw material's content should be between 100% and 103%!"

    @staticmethod
    def save_not_existing_raw_materials(formset, all_raw_materials):
        raw_materials_name_list = list(all_raw_materials.values_list("trade_name", flat=True))
        for form in formset:
            current_raw_material = form.cleaned_data.get("current_trade_name")

            if current_raw_material in raw_materials_name_list:
                continue
            else:
                form.save()

    def save_natural_origin_content(self, natural_content):

        """
        Save natural origin content to PRODUCT.
        """

        product_id = self.request.session.get("product_id")
        product = get_object_or_404(Product, pk=product_id)

        product.natural_content = natural_content
        product.edited_on = timezone.now()
        product.save()

    def save_formula_recipe(self, raw_materials, action, natural_content):

        """
        Save natural origin content and raw materials to the formula.
        Delete old instances of the formula if formula is updated and save the new formula.
        """

        formula_id = self.request.session.get("formula_id")
        formula = ProductFormula.objects.prefetch_related("formula__raw_material").get(pk=formula_id)
        formula.formula_natural_content = natural_content
        formula.save()

        all_raw_materials = RawMaterial.objects.all()

        if action == "update":

            formula_materials_to_delete = [material.id for material in formula.formula.all()]
            ProductFormulaRawMaterial.objects.filter(id__in=formula_materials_to_delete).delete()

        raw_material_objects = []
        for raw_material in raw_materials:
            raw_material_content = raw_material.cleaned_data.get("raw_material_content")
            raw_material_trade_name = raw_material.cleaned_data.get("current_trade_name")
            raw_material_object = all_raw_materials.get(trade_name=raw_material_trade_name)

            raw_material_objects.append(
                ProductFormulaRawMaterial(
                    raw_material_content=raw_material_content,
                    formula=formula,
                    raw_material=raw_material_object,
                )
            )

        ProductFormulaRawMaterial.objects.bulk_create(raw_material_objects)

    def calculate_product_natural_content(self, raw_materials, all_raw_materials):
        product_raw_natural_content = []
        sum_off_raw_materials_content = 0

        for raw_material in raw_materials:

            current_raw_material_name = raw_material.cleaned_data.get("current_trade_name")
            content_in_formulation = raw_material.cleaned_data.get("raw_material_content")
            natural_origin_content = all_raw_materials.get(trade_name=current_raw_material_name).natural_origin_content

            sum_off_raw_materials_content += content_in_formulation
            calculated = content_in_formulation * natural_origin_content / 100
            product_raw_natural_content.append(calculated)

        if (sum_off_raw_materials_content > self.MAXIMUM_SUM_OF_CONTENT
                or sum_off_raw_materials_content < self.MINIMUM_SUM_OF_CONTENT):
            return None

        product_natural_content = (sum(product_raw_natural_content) / sum_off_raw_materials_content) * 100

        return product_natural_content


class OwnerRequiredMixin(auth_mixins.LoginRequiredMixin):

    """Verify that the current user has this product."""

    owner_field = "owner_id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj_user = getattr(obj, self.owner_field, None)
        if obj_user != self.request.user.id:
            raise exceptions.PermissionDenied

        return obj


