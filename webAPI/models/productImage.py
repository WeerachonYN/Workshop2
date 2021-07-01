from django.db import models
from webAPI.models.product import Product
from versatileimagefield.fields import VersatileImageField

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name= 'product_image',default=None,null=True)
    image = VersatileImageField(max_length=255,upload_to='images/Image_products',default='',blank=True, null=True)

    def __str__(self):
            return self.product.name