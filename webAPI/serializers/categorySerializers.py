from rest_framework import serializers
from webAPI.models.category import Category
from versatileimagefield.serializers import VersatileImageFieldSerializer
class categorySerializers(serializers.ModelSerializer):
    products = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True)
    image = VersatileImageFieldSerializer(
        sizes='headshot'
    )
    class Meta:
        model = Category
        fields = ['id','name','image','detail','is_enabled','products']