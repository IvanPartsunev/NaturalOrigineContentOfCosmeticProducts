from django.contrib.auth import get_user_model
from django.urls import reverse

from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountModel
from NaturalOriginContentOfCosmeticProducts.accounts.views import AccountCreateView
from NaturalOriginContentOfCosmeticProducts.products.models import Product
from NaturalOriginContentOfCosmeticProducts.tests.test_base import TestBase

UserModel = get_user_model()
class ProductDetailsViewTest(TestBase):
    def setUp(self):
        self.user = self._create_user()

        self.owner = self.user
        self.non_owner = AccountModel.objects.create_user(
            email='nonowner@example.com', company_name="nonownercompany", password='nonownerpassword3344')

        self.product = Product.objects.create(product_name="Test Product", owner=self.owner)
        self.url = reverse("product_details", kwargs={"pk": self.product.pk})

    def test_access_denied_for_non_owner(self):
        self.client.login(email='nonowner@example.com', password='nonownerpassword3344')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_for_owner(self):
        self.client.login(**self.USER_DATA)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_session_data_set_correctly(self):
        self.client.login(**self.USER_DATA)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.client.session.get("product_name"), self.product.product_name)
        self.assertEqual(self.client.session.get("product_id"), self.product.pk)
