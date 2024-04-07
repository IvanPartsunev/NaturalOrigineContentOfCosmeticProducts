from django.contrib.auth import get_user_model
from django.urls import reverse

from NaturalOriginContentOfCosmeticProducts.accounts.models import AccountModel
from NaturalOriginContentOfCosmeticProducts.products.models import Product, ProductFormula, ProductFormulaRawMaterial
from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial
from NaturalOriginContentOfCosmeticProducts.tests.test_base import TestBase

UserModel = get_user_model()


class ProductFormulaDetailsViewTest(TestBase):
    def setUp(self):
        self.user = self._create_user()
        self.client.login(**self.USER_DATA)

        self.owner = self.user
        self.product = Product.objects.create(product_name="Test Product", owner=self.owner)
        self.product_formula = ProductFormula.objects.create(
            description="Test Formula",
            product=self.product,
            is_active=True,
            owner=self.owner,
        )

        self.raw_material = RawMaterial.objects.create(
            trade_name="Test Raw Material",
            inci_name="Test INCI",
            material_type="Test Material Type",
            natural_origin_content=0,
        )

        self.formula_raw_materials = ProductFormulaRawMaterial.objects.create(
            raw_material_content=100,
            formula=self.product_formula,
            raw_material=self.raw_material,
        )
        self.url = reverse("product_formula_details", kwargs={"pk": self.product.pk})

    def test_access_denied_for_non_owner(self):
        AccountModel.objects.create_user(
            email='nonowner@example.com', company_name="nonownercompany", password='nonownerpassword3344'
        )

        self.client.login(email='nonowner@example.com', password='nonownerpassword3344')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_for_owner(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_session_data_set_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.client.session.get("formula_id"), self.product_formula.pk)
        self.assertEqual(self.client.session.get("formula_description"), self.product_formula.description)

    def test_formset_initialized_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        formset = response.context["formset"]
        self.assertEqual(len(formset.forms), 1)
        self.assertEqual(formset.forms[0].initial["current_trade_name"], self.raw_material.trade_name)
        self.assertEqual(formset.forms[0].initial["inci_name"], self.raw_material.inci_name)
        self.assertEqual(formset.forms[0].initial["raw_material_content"], self.formula_raw_materials.raw_material_content)
        self.assertEqual(formset.forms[0].initial["material_type"], self.raw_material.material_type)
        self.assertEqual(formset.forms[0].initial["natural_origin_content"], self.raw_material.natural_origin_content)
