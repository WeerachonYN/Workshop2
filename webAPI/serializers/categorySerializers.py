from rest_framework import serializers
from webAPI.models.category import Category

class categorySerializers(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True)
    class Meta:
        model = Category
        fields = ['id','name','image','detail','is_enabled','products']