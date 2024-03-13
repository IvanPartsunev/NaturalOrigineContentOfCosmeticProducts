from django.apps import AppConfig


class UserAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NaturalOriginContentOfCosmeticProducts.accounts'

    def ready(self):
        import NaturalOriginContentOfCosmeticProducts.accounts.signals
