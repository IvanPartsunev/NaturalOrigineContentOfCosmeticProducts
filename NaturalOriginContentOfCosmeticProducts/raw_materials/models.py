from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from NaturalOriginContentOfCosmeticProducts.core.mixins import CreateUpdateMixin


class RawMaterial(CreateUpdateMixin):
    MAX_NATURAL_ORIGIN_CONTENT = 100
    MIN_NATURAL_ORIGIN_CONTENT = 0

    class NaturalTypeChoices(models.TextChoices):
        NATURAL = "NA", _("Natural")
        NATURAL_DERIVED = "ND", _("Natural derived")
        NON_NATURAL = "NN", _("Non natural")

    trade_name = models.CharField(
        unique=True,
        blank=False,
        null=False,
    )
    inci_name = models.CharField(
        blank=False,
        null=False,
    )

    material_type = models.CharField(
        choices=NaturalTypeChoices
    )

    natural_origin_content = models.IntegerField(
        validators=[
            MaxValueValidator(MAX_NATURAL_ORIGIN_CONTENT),
            MinValueValidator(MIN_NATURAL_ORIGIN_CONTENT)
        ],
        blank=False,
        null=False,
    )

    is_deleted = models.BooleanField(
        default=False,
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.trade_name
