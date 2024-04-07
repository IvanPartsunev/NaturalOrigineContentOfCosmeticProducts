from django.urls import reverse

from NaturalOriginContentOfCosmeticProducts.core.forms import SearchForm
from NaturalOriginContentOfCosmeticProducts.tests.test_base import TestBase


class ProductListViewTest(TestBase):
    def setUp(self):
        self.user = self._create_user()
        self.client.login(**self.USER_DATA)
        self.url = reverse("product_list")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")

    def test_access_granted_for_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_session_data_reset(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.client.session.get("product_name"))
        self.assertIsNone(self.client.session.get("product_id"))

    def test_context_data(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Ensure successful access
        self.assertIn("search_form", response.context)  # Check if search form is included in the context
        self.assertIsInstance(response.context["search_form"], SearchForm)  # Verify search form type