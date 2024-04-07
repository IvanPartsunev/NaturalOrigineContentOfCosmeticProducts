from django.contrib.auth import get_user_model
from django.test import TestCase

from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountModel

UserModel = get_user_model()


class TestBase(TestCase):
    USER_DATA = {
        "email": "test_case_email@gmail.com",
        "company_name": "Test company inc",
        "password": "poweroverwhelming222222"
    }

    def _create_user(self):
        return AccountModel.objects.create_user(**self.USER_DATA)
