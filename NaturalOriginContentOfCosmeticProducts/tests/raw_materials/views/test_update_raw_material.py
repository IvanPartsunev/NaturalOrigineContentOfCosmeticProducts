from django.urls import reverse

from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial
from NaturalOriginContentOfCosmeticProducts.tests.test_base import TestBase


class RawMaterialUpdateViewTest(TestBase):

    def setUp(self):
        self._create_user()
        self.client.login(**self.USER_DATA)

        self.raw_material = RawMaterial.objects.create(
            trade_name="Test Raw Material", inci_name="Test INCI", material_type="ND", natural_origin_content=90
        )

    def test_view_returns_correct_template(self):
        url = reverse("raw_material_update", kwargs={"pk": self.raw_material.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "raw_materials/raw-material-update.html")

    def test_get_object_with_initial_pk(self):
        """
        Test if an object is retrieved when initial_pk is provided in GET request
        """

        url = reverse("raw_material_update", kwargs={"pk": self.raw_material.pk})
        response = self.client.get(url, {"raw_material": self.raw_material.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.raw_material)

    def test_get_object_without_initial_pk(self):
        """
        Test if an object is retrieved when initial_pk is not provided
        """

        url = reverse("raw_material_update", kwargs={"pk": self.raw_material.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.raw_material)

    def test_get_success_url(self):
        """
        Test if the view redirects to the correct URL after form submission
        """

        url = reverse("raw_material_update", kwargs={"pk": self.raw_material.pk})
        response = self.client.post(
            url, {
                "trade_name": "Updated Trade Name",
                "inci_name": "Updated INCI",
                "material_type": "ND",
                "natural_origin_content": 90}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("raw_material_details", kwargs={"pk": self.raw_material.pk}))

    def test_context_data(self):
        """
        Test if existing materials are included in the context
        """

        url = reverse("raw_material_update", kwargs={"pk": self.raw_material.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("existing_materials" in response.context)
        self.assertQuerysetEqual(
            response.context["existing_materials"],
            RawMaterial.objects.all(),
            transform=lambda x: x
        )