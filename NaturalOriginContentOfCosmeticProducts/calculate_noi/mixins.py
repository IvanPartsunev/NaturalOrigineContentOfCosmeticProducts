from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404

from NaturalOriginContentOfCosmeticProducts.calculate_noi.models import Product, ProductFormula, \
    ProductFormulaRawMaterial
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class CalculateSaveMixin:
    MINIMUM_SUM_OF_CONTENT = 100
    MAXIMUM_SUM_OF_CONTENT = 103

    @staticmethod
    def save_not_existing_raw_materials(formset):
        all_raw_materials = RawMaterial.objects.values_list("trade_name", flat=True)
        for form in formset:
            if form.cleaned_data.get("current_trade_name") in all_raw_materials:
                continue
            else:
                form.save()

    def save_natural_origin_content(self, natural_content):
        product_id = self.request.session.get("product_id")
        product = get_object_or_404(Product, pk=product_id)

        product.natural_content = natural_content
        product.save()

    def save_formula_recipe(self, raw_materials):
        all_raw_materials = RawMaterial.objects.all()
        formula_id = self.request.session.get("formula_id")
        formula = ProductFormula.objects.get(pk=formula_id)
        formula_content = []
        for raw_material in raw_materials:
            raw_material_content = raw_material.cleaned_data.get("raw_material_content")
            raw_material_trade_name = raw_material.cleaned_data.get("current_trade_name")
            raw_material_object = all_raw_materials.get(trade_name=raw_material_trade_name)

            formula_content.append(
                ProductFormulaRawMaterial(
                    raw_material_content=raw_material_content,
                    formula=formula,
                    raw_material=raw_material_object,
                )
            )

        ProductFormula.objects.bulk_create(formula_content)

    def calculate_product_natural_content(self, raw_materials):
        product_raw_natural_content = []
        sum_off_raw_materials_content = 0

        for raw_material in raw_materials:
            content_in_formulation = raw_material.cleaned_data.get("raw_material_content")
            natural_origin_content = raw_material.cleaned_data.get("natural_origin_content")

            sum_off_raw_materials_content += content_in_formulation
            calculated = content_in_formulation * natural_origin_content / 100
            product_raw_natural_content.append(calculated)

        if self.MAXIMUM_SUM_OF_CONTENT < sum_off_raw_materials_content < self.MINIMUM_SUM_OF_CONTENT:
            return None

        product_natural_content = (sum(product_raw_natural_content) / sum_off_raw_materials_content) * 100

        return product_natural_content


class OwnerRequiredMixin(AccessMixin):
    """Verify that the current user has this product."""
    permission_denied_message = "You are not authorized to open this page!"

    def dispatch(self, request, *args, **kwargs):
        product = Product.objects.filter(pk=kwargs.get('pk', None)).first()
        if request.user.pk != product.owner_id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
