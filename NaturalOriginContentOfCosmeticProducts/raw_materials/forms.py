import re

from django import forms
from django.core.exceptions import ValidationError

from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class RawMaterialForm(forms.ModelForm):
    REGEX_PATTERN = re.compile(r"[a-zA-Z-0-9]+")
    REGEX_SPLIT = r"[ and ]{5,}|[ \(and\) ]{7,}|[, ]{2,}"

    class Meta:
        model = RawMaterial
        fields = [
            "trade_name",
            "inci_name",
            "material_type",
            "natural_origin_content",
        ]

        labels = {
            "trade_name": "Trade name:",
            "inci_name": "INCI:",
            "material_type": "Type:",
            "natural_origin_content": "Natural origin content in %:"
        }

    def clean_trade_name(self):
        data = self.cleaned_data.get("trade_name")
        split_data = re.findall(self.REGEX_PATTERN, data)
        cleared_trade_name = " ".join(x.upper() for x in split_data)

        if not cleared_trade_name:
            raise ValidationError('Invalid Trade name')
        return cleared_trade_name

    def clean_inci_name(self):
        data = self.cleaned_data.get("inci_name")
        cleared_inci_name = ", ".join(re.split(self.REGEX_SPLIT, data))

        if not cleared_inci_name:
            raise ValidationError('Invalid INCI name')

        return cleared_inci_name

    def clean_natural_origin_content(self):
        data = self.cleaned_data.get("natural_origin_content")

        cleared_natural_origin_content = int(data)

        if cleared_natural_origin_content is None:
            raise ValidationError('Invalid value for natural origin content')

        return cleared_natural_origin_content
