from rest_framework import serializers
from webAPI.models.product import Product
from webAPI.exception import custom_exception_handler
from webAPI.serializers.productImageSerializers import ProductImageSerializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
class Product_ListSerializers(serializers.ModelSerializer):
    # category = Product.objects.filter(category__in=(1,2))
    class Meta:
        model = Product
        fields = ['url','id','category','name','price','detail','image','is_enabled','created_datetime']

class Product_DetailSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(many=True,  read_only=True)
    # product_image = VersatileImageFieldSerializer(
    #     sizes=[
    #         # ('full_size', 'url'),
    #         # ('thumbnail', 'thumbnail__100x100'),
    #         # ('medium_square_crop', 'crop__400x400'),
    #         # ('small_square_crop', 'crop__50x50')
    #     ]
    # )
    # category = Product.objects.filter(category__in=(1,2))
    class Meta:
        model = Product
        fields = ['url','id','category','name','price','detail','image','is_enabled','created_datetime','product_image']