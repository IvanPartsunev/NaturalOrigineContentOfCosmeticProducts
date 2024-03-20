from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from NaturalOriginContentOfCosmeticProducts.core.mixins import CreateUpdateMixin
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial


class Product(CreateUpdateMixin):

    product_name = models.CharField(
        unique=True,
        blank=False,
        null=False,
    )

    natural_content = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ]
    )


class ProductFormula(CreateUpdateMixin):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )


class ProductFormulaRawMaterial(models.Model):

    raw_material_content = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )

    formula = models.ForeignKey(
        ProductFormula,
        on_delete=models.CASCADE,
        related_name="formula",
    )

    raw_material = models.OneToOneField(
        RawMaterial,
        on_delete=models.CASCADE,
    )


