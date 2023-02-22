from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_list", kwargs={"category": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


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

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk, "category": self.category.slug})


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.body} - {self.order}"
