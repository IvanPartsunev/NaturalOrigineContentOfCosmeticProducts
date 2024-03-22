from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models

from NaturalOriginContentOfCosmeticProducts.accounts.managers import NaturalOriginAccountManager


class AccountModel(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    company_name = models.CharField(
        _("company name"),
        max_length=150,
        unique=True,
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = NaturalOriginAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["company_name",]

    def __str__(self):
        return self.company_name


class AccountProfileModel(models.Model):

    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        null=True,
    )

    company_website = models.URLField(
        _("company website"),
        blank=True,
        null=True,
    )

    company_logo = models.URLField(
        _("company logo"),
        blank=True,
        null=True,
    )

    company = models.OneToOneField(
        AccountModel,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    @property
    def get_full_name(self):
        if not self.first_name or not self.last_name:
            return "Name not entered. Update profile."
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
