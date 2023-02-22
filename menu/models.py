from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=150)
    #It is a SlugField which is not nullable and must be unique.
    slug = models.SlugField(null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #This method defines how the category should be displayed as a string. 
    # In this case, it will return the name of the category
    #self refers to the instance of the class itself. 
    # It is used to access the instance's variables and methods within the class.
    def __str__(self):
        return self.name
    #This method defines the URL of the category detail page. 
    # It uses the reverse function to reverse the URL pattern named item_list and pass the category slug as a keyword argument.

    def get_absolute_url(self):
        return reverse("item_list", kwargs={"category": self.slug})
    #This method is a custom save method which is called whenever a category object is saved. 
    # It checks if the slug is not set and generates it using the slugify function based on the category name. 
    # Then it calls the save method of the superclass to actually save the object.
    def save(self, *args, **kwargs):  # new
        # args-->is used to pass a variable number of arguments to a method .
        #it allows me to passs any number of positional to the methodand they are collect in tuple .
        #kwargs---->the sme ags but return dictionary 
        if not self.slug:
            self.slug = slugify(self.name)
            #In object-oriented programming, super() is a built-in Python function 
            # that allows you to call a method of a parent class from a subclass.
        return super().save(*args, **kwargs)

"""
the perviouse  model class represents a category with a name, slug, created_at, updated_at fields, 
and provides methods for displaying and generating the URL of the category detail page. 
The custom save method ensures that the slug is always generated based on the category name.
"""
class Item(models.Model):
   # This is a foreign key field that creates a many-to-one relationship between an Item instance and a Category instance. T
    #this allows you to associate each item with a category.
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
    #This method returns the absolute URL of the item's detail page.
    #  The reverse() function is used to generate the URL based on the name of the view and any required parameters, such as the item's primary key (pk) and its category's slug.

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
    def get_absolute_url(self):
        return reverse("order", kwargs={"pk": self.pk})
    


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.body} - {self.order}"
