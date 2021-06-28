from django.db import models
from webAPI.models.category import Category

class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name= 'products',default=None,null=True)
    price = models.FloatField()
    detail = models.CharField(max_length=225)
    image= models.ImageField(max_length=255,upload_to='images/products',default='',blank=True, null=True)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
            return self.name