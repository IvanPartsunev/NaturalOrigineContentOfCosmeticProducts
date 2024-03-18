from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import formset_factory

from NaturalOriginContentOfCosmeticProducts.raw_materials.forms import RawMaterialForm
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class CalculateNaturalContentForm(RawMaterialForm):
    MIN_RAW_MATERIAL_CONTENT = 0
    MAX_RAW_MATERIAL_CONTENT = 100

    raw_material_content = forms.IntegerField(
        label="Content in %",
        validators=[
            MinValueValidator(MIN_RAW_MATERIAL_CONTENT),
            MaxValueValidator(MAX_RAW_MATERIAL_CONTENT),
        ]
    )

    class Meta(RawMaterialForm.Meta):
        model = RawMaterial
        fields = [
            "trade_name",
            "inci_name",
            "raw_material_content",
            "material_type",
            "natural_origin_content"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field = self.fields.get(key)
            field.widget.attrs.update({'placeholder': field.label})
            field.label = ""


MyFormSet = formset_factory(CalculateNaturalContentForm, extra=1)
