from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/items/')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.updated_at}"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    table_num = models.IntegerField()
    receive_time = models.DateTimeField(blank=True, null=True)
    total_price = models.FloatField()
    order_accept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.table_num} , {self.receive_time}"


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return f"{self.body} - {self.order}"
