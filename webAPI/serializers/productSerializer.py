from rest_framework import serializers
from webAPI.models.product import Product
from webAPI.exception import custom_exception_handler
from webAPI.serializers.productImageSerializers import ProductImageSerializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
class Product_ListSerializers(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='headshot')    
    class Meta:
        model = Product
        fields = ['url','id','category','name','price','detail','image','is_enabled','created_datetime']

class Product_DetailSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(many=True,  read_only=True)
    image = VersatileImageFieldSerializer(
        sizes='headshot'
    )
    # category = Product.objects.filter(category__in=(1,2))
    class Meta:
        model = Product
        fields = ['url','id','category','name','price','detail','image','is_enabled','created_datetime','product_image']