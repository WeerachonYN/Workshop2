from rest_framework import serializers
from webAPI.models.product import Product
from webAPI.exception import custom_exception_handler
from webAPI.serializers.productImageSerializers import ProductImageSerializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from webAPI.serializers.CommentSerializer import CommentSerializer
class Product_ListSerializers(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,  read_only=True)
    image = VersatileImageFieldSerializer(
        sizes='headshot')    
    class Meta:
        model = Product
        fields = ['url','id','category','name','price','detail','image','is_enabled','created_datetime','comments']

class Product_DetailSerializers(serializers.ModelSerializer):
    product_image = ProductImageSerializers(many=True,  read_only=True)
    image = VersatileImageFieldSerializer(
        sizes='headshot'
    )
    category_name = serializers.SerializerMethodField()
    # category = Product.objects.filter(category__in=(1,2))
    class Meta:
        model = Product
        fields = ['url','id','category','category_name','name','price','detail','image','is_enabled','created_datetime','product_image']
    
    def get_category_name(self,obj):
        return obj.category.name
class Product_CARTSerializers(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    image = VersatileImageFieldSerializer(
        sizes='headshot'
        )
    class Meta:
        model = Product
        fields = ['id','name','price','image','detail','category','category_id']
    def get_category(self,obj):
        return obj.category.name
    def get_category_id(self,obj):
        return obj.category.id