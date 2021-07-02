from django.db import models
from webAPI.models.product import Product
from versatileimagefield.fields import VersatileImageField,PPOIField

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name= 'product_image',default=None,null=True)
    # image = VersatileImageField(max_length=255,upload_to='images/Image_products',default='',blank=True, null=True)
    image = VersatileImageField(
        'Headshot',
        upload_to='headshots/products_image/',
        ppoi_field='headshot_ppoi'
    )
    headshot_ppoi = PPOIField()

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'products_images_headshot'
    def __str__(self):
            return self.product.name