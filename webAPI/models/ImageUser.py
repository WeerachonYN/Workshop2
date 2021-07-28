from django.db import models
from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField,PPOIField

class ImageUser(models.Model):
    user = models.OneToOneField(User, related_name='images',
                            on_delete=models.CASCADE, default=None, null=True)
    image = VersatileImageField(
        'Headshot',
        upload_to='headshots/User/',
        ppoi_field='headshot_ppoi'
    )
    headshot_ppoi = PPOIField()
    class Meta:
        verbose_name = 'UserImage'
        verbose_name_plural = 'UsersImage'
    
    def __str__(self):
            return self.user.username