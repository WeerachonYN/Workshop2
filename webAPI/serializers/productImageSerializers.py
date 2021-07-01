from rest_framework import serializers
from webAPI.models.productImage import ProductImage
from versatileimagefield.serializers import VersatileImageFieldSerializer

class ProductImageSerializers(serializers.ModelSerializer):
    # headshot = VersatileImageFieldSerializer(
    #     sizes=[
    #         ('full_size', 'url'),
    #         ('thumbnail', 'thumbnail__100x100'),
    #         ('medium_square_crop', 'crop__400x400'),
    #         ('small_square_crop', 'crop__50x50')
    #     ]
    # )
    class Meta:
        model = ProductImage
        fields = ['id','product','image']