from rest_framework import serializers
from webAPI.models.product import Product

class ProductSerializers(serializers.ModelSerializer):
    product_image = serializers.HyperlinkedRelatedField(many=True, view_name='product_image-detail', read_only=True)
    # category = Product.objects.filter(category__in=(1,2))
    class Meta:
        model = Product
        fields = ['url','id','category','name','price','detail','image','is_enabled','product_image']