from rest_framework import serializers
from webAPI.models.productImage import ProductImage

class ProductImageSerializers(serializers.ModelSerializer):
   
    class Meta:
        model = ProductImage
        fields = ['id','product','image']