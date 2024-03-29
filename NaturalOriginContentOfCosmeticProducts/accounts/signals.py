from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountProfileModel

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def company_account_create_profile(sender, instance, created, **kwargs):
    if created:
        AccountProfileModel.objects.create(company=instance)
