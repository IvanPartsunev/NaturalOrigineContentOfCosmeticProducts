from django.urls import reverse

from NaturalOriginContentOfCosmeticProducts.products.forms import ProductCreateForm
from NaturalOriginContentOfCosmeticProducts.products.models import Product
from NaturalOriginContentOfCosmeticProducts.products.views import ProductCreateView
from NaturalOriginContentOfCosmeticProducts.tests.test_base import TestBase


class ProductCreateViewTest(TestBase):
    def setUp(self):
        self.user = self._create_user()
        self.client.login(**self.USER_DATA)

        self.url = reverse("product_create")
        self.valid_data = {
            "product_name": "Test Product",
            "owner": self.user,
        }

    def test_view_returns_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product-create.html")

    def test_create_product(self):
        """
        View should redirect after successful form submission,
        check if the product was created,
        check if the owner is set correctly
        """
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.exists())
        product = Product.objects.first()
        self.assertEqual(product.owner, self.user)

    def test_get_success_url(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        product = Product.objects.first()
        self.assertEqual(response.url, reverse("product_details", kwargs={"pk": product.pk}))

    def test_form_valid_sets_owner(self):
        form = ProductCreateForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        view = ProductCreateView()
        view.request = self.client.get(self.url)
        view.request.user = self.user
        view.form_valid(form)

        self.assertTrue(Product.objects.exists())
        product = Product.objects.first()
        self.assertEqual(product.owner, self.user)
