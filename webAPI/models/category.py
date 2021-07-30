from django.db import models
from versatileimagefield.fields import VersatileImageField,PPOIField

class Category(models.Model):
    name = models.CharField(max_length=50)
    detail = models.CharField(max_length=225)
    is_enabled = models.BooleanField(default=True)
    image = VersatileImageField(
        'Headshot',
        upload_to='headshots/category/',
        ppoi_field='headshot_ppoi'
    )
    headshot_ppoi = PPOIField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
    def __str__(self):
            return self.name