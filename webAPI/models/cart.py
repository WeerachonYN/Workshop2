from django.db import models
from django.contrib.auth.models import User
from webAPI.models.product import Product
from decimal import Decimal
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='carts_products',default=None,null=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE,related_name='carts_users',default=None,null=True)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=7, decimal_places=2,default=Decimal('0.00'))
    
    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return self.product.name
