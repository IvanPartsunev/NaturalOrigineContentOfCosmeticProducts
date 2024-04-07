from django.contrib.auth import get_user_model
from django.urls import reverse

from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial
from NaturalOriginContentOfCosmeticProducts.tests.test_base import TestBase


class RawMaterialCreateViewTest(TestBase):
    def setUp(self):
        self._create_user()
        self.client.login(**self.USER_DATA)

        self.url = reverse("raw_material_create")
        self.valid_data = {
            "trade_name": "CETIOL CC",
            "inci_name": "Dicaprylyl Carbonate",
            "material_type": "NN",
            "natural_origin_content": 100,
        }

    def test_form_valid_with_material_type_NN(self):
        """
        Test form_valid method of RawMaterialCreateView when material_type is 'NN'.
        """

        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful form submission
        self.assertEqual(RawMaterial.objects.last().natural_origin_content, 0)

    def test_form_valid_with_material_type_other_than_NN(self):
        """
        Test form_valid method of RawMaterialCreateView when material_type is not 'NN'.
        """

        self.valid_data["material_type"] = "ND"
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(RawMaterial.objects.last().natural_origin_content, 0)

    def test_form_invalid(self):
        """
        Test form_valid method of RawMaterialCreateView with invalid data.
        """

        invalid_data = {
            "trade_name": "CETIOL CC",
            "inci_name": "Dicaprylyl Carbonate",
            "material_type": "NN",
            "natural_origin_content": 200,
        }

        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(RawMaterial.objects.count(), 1)
