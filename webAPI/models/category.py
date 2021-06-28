from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(max_length=255,upload_to='image/categorys',default='',blank=True, null=True)
    detail = models.CharField(max_length=225)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
            return self.name