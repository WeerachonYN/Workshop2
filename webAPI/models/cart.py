from django.db import models
from django.contrib.auth.models import User
from webAPI.models.product import Product

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name= 'carts_products',default=None,null=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name='carts_users',default=None,null=True)
    quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name