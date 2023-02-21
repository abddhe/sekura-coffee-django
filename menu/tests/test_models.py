from django.test import TestCase
from menu.models import (Category, Item, Order, Comment)


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="hot")

    def test_string_method(self):
        category = Category.objects.get(pk=1)
        expected_string = category.name
        self.assertEqual(str(category), expected_string)


class ItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="hot")
        Item.objects.create(category=category, name="coffee", description="hot drink", price=100.0)

    def test_string_method(self):
        item = Item.objects.get(pk=1)
        expected_string = f"{item.name} - {item.updated_at}"
        self.assertEqual(str(item), expected_string)


class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="hot")
        item = Item.objects.create(category=category, name="coffee", description="hot drink", price=100.0)
        item1 = Item.objects.create(category=category, name="coffee_1", description="hot drink_1", price=100.0)
        order = Order.objects.create(table_num=1, order_accept=True, total_price=200.0)
        order.items.set([item, item1])

    def test_string_method(self):
        order = Order.objects.get(pk=1)
        expected_string = f"{order.table_num} , {order.receive_time}"
        self.assertEqual(str(order), expected_string)


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="hot")
        item = Item.objects.create(category=category, name="coffee", description="hot drink", price=100.0)
        item1 = Item.objects.create(category=category, name="coffee_1", description="hot drink_1", price=100.0)
        order = Order.objects.create(table_num=1, order_accept=True, total_price=200.0)
        order.items.set([item, item1])
        Comment.objects.create(order=order, body="with milk")

    def test_string_method(self):
        comment = Comment.objects.get(pk=1)
        expected_string = f"{comment.body} - {comment.order}"
        self.assertEqual(str(comment), expected_string)
