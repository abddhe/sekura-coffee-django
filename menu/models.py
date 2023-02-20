from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/items/')
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self) -> str:
        return f"{self.name} - {self.updated_at}"