from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=150)
    # It is a SlugField which is not nullable and must be unique.
    slug = models.SlugField(blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # This method defines how the category should be displayed as a string.
    # In this case, it will return the name of the category
    # self refers to the instance of the class itself.
    # It is used to access the instance's variables and methods within the class.
    def __str__(self):
        return self.name

    # This method defines the URL of the category detail page.
    # It uses the reverse function to reverse the URL pattern named item_list and pass the category slug as a keyword argument.

    def get_absolute_url(self):
        return reverse("item_list", kwargs={"category": self.slug})

    # This method is a custom save method which is called whenever a category object is saved.
    # It checks if the slug is not set and generates it using the slugify function based on the category name. 
    # Then it calls the save method of the superclass to actually save the object.
    def save(self, *args, **kwargs):  # new
        # args-->is used to pass a variable number of arguments to a method .
        # it allows me to pass any number of positional to the method and they are collect in tuple .
        # kwargs---->the sme ags but return dictionary
        if not self.slug:
            self.slug = slugify(self.name)
            # In object-oriented programming, super() is a built-in Python function
            # that allows you to call a method of a parent class from a subclass.
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


class Table(models.Model):
    number = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"The table #{self.number}"


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    receive_time = models.TimeField(blank=True, null=True)
    total_price = models.FloatField(blank=True, default=0)
    ordered = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    order_accept = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, using=None, keep_parents=False, force_delete=False):
        if self.canceled or force_delete:
            return super().delete()
        self.canceled = True
        self.save(using=using)

    def __str__(self):
        return f"{self.table} , {self.receive_time}"

    def get_absolute_url(self):
        return reverse("order", kwargs={"pk": self.pk})


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order}"


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.body} - {self.order}"


class Notification(models.Model):
    MESSAGE = "message"
    ORDER = 'order'
    COMMENT = 'comment'
    CHOICES = [
        (0, MESSAGE),
        (1, ORDER),
        (2, COMMENT),
    ]
    body = models.TextField()
    type = models.IntegerField(choices=CHOICES)
    opened = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body
