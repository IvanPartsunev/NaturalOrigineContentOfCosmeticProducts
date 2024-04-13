from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountModel
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
        ],
        blank=True,
        null=True,
    )

    owner = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.product_name


class ProductFormula(CreateUpdateMixin):
    description = models.CharField(
        max_length=255,
        verbose_name="Formula description",
        blank=True,
        null=True,
    )

    formula_natural_content = models.IntegerField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ],
        blank=True,
        null=True,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="product",
    )

    is_active = models.BooleanField(
        default=False,
        blank=False,
        null=False,
    )

    owner = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.product} formula"
    

class ProductFormulaRawMaterial(CreateUpdateMixin):

    raw_material_content = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
    )

    formula = models.ForeignKey(
        ProductFormula,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="formula",
    )

    raw_material = models.ForeignKey(
        RawMaterial,
        on_delete=models.RESTRICT,
        blank=False,
        null=False,
        related_name="raw_materials",
    )

    def __str__(self):
        return f"Raw material for {self.formula}"

