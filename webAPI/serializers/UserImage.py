from webAPI.models.ImageUser import ImageUser
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
class ImageUserSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='headshot'
    )
    class Meta:
        model = ImageUser
        fields = ['user','image']
   