from django.urls import reverse

from NaturalOriginContentOfCosmeticProducts.raw_materials.models import RawMaterial
from NaturalOriginContentOfCosmeticProducts.tests.test_base import TestBase


class RawMaterialListViewTest(TestBase):
    def setUp(self):

        self.url = reverse("raw_material_list")
        self.raw_materials = [
            RawMaterial.objects.create(
                trade_name="Test 1", inci_name="Test INCI 1", material_type="ND", natural_origin_content=90
            ),
            RawMaterial.objects.create(
                trade_name="Test 2", inci_name="Test INCI 2", material_type="ND", natural_origin_content=90
            ),
            RawMaterial.objects.create(
                trade_name="Another", inci_name="Another", material_type="ND", natural_origin_content=90
            ),
        ]

    def test_view_returns_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "raw_materials/raw-material-list.html")

    def test_pagination_assert_paginated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("paginator" in response.context_data)
        self.assertTrue("page_obj" in response.context_data)

    def test_queryset_filtering(self):
        """
        Test search bar filtering.
        """
        response = self.client.get(self.url, {"search_query": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["object_list"]), 2)

        response = self.client.get(self.url, {"search_query": "INCI"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data["object_list"]), 2)

    def test_context_data(self):
        """
        Check the view is returning the search query.
        """
        response = self.client.get(self.url, {"search_query": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["search_query"], "Test")
