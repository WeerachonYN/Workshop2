from django.db import models
from webAPI.models.category import Category
from versatileimagefield.fields import VersatileImageField,PPOIField
import datetime
class Product(models.Model):
    name = models.CharField(max_length=50,)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name= 'products',default=None,null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    detail = models.CharField(max_length=225)
#     image= VersatileImageField(max_length=255,upload_to='images/products',default='',blank=True, null=True)
    is_enabled = models.BooleanField(default=True)
    recommend = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now=True)
    image = VersatileImageField(
        'Headshot',
        upload_to='headshots/product/',
        ppoi_field='headshot_ppoi'
    )
    headshot_ppoi = PPOIField()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
            self.updated_datetime = datetime.datetime.now()
            super().save(*args, **kwargs)

    def __str__(self):
            return self.name
