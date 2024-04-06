import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import formset_factory, BaseFormSet

from NaturalOriginContentOfCosmeticProducts.products.models import Product
from NaturalOriginContentOfCosmeticProducts.raw_materials.forms import RawMaterialForm
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "product_name",
        ]


class ProductCalculateNaturalContentForm(RawMaterialForm):
    MIN_RAW_MATERIAL_CONTENT = 0
    MAX_RAW_MATERIAL_CONTENT = 100

    current_trade_name = forms.CharField(
        label="Trade name"
    )

    raw_material_content = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        label="%",
        validators=[
            MinValueValidator(MIN_RAW_MATERIAL_CONTENT),
            MaxValueValidator(MAX_RAW_MATERIAL_CONTENT),
        ]
    )

    class Meta(RawMaterialForm.Meta):
        model = RawMaterial
        fields = [
            "current_trade_name",
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
            # field.label = ""

    def clean_current_trade_name(self):
        data = self.cleaned_data.get("current_trade_name")
        split_data = re.findall(self.REGEX_PATTERN, data)
        cleared_trade_name = " ".join(x.upper() for x in split_data)

        if not cleared_trade_name:
            raise ValidationError('Invalid Trade name')
        return cleared_trade_name

    def save(self, commit=True):
        RawMaterial.objects.create(
            trade_name=self.cleaned_data.get("current_trade_name"),
            inci_name=self.cleaned_data.get("inci_name"),
            material_type=self.cleaned_data.get("material_type"),
            natural_origin_content=self.cleaned_data.get("natural_origin_content"),
        )


MyFormSet = formset_factory(ProductCalculateNaturalContentForm, extra=1)
