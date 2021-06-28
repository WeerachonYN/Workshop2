from django.db import models
from webAPI.models.product import Product

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name= 'product_image',default=None,null=True)
    image = models.ImageField(max_length=255,upload_to='images/Image_products',default='',blank=True, null=True)

    def __str__(self):
            return self.product.name