from django.test import TestCase
from menu.models import (Item, Category)
from django.urls import reverse


class ItemUrlsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="hot")
        Item.objects.create(name="coffee", description="hot drink", price=1000, category=category)

    def test_url_exists(self):
        category = Category.objects.get(pk=1)
        response = self.client.get(f"/menu/{category.slug}/1")
        self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        category = Category.objects.get(pk=1)
        response = self.client.get(reverse('item_list', kwargs={'category': category.slug}))
        self.assertEqual(response.status_code, 200)
