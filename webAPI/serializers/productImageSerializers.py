from rest_framework import serializers
from webAPI.models.productImage import ProductImage
from versatileimagefield.serializers import VersatileImageFieldSerializer

class ProductImageSerializers(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='headshot'
    )
    class Meta:
        model = ProductImage
        fields = ['id','product','image']