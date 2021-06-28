from rest_framework import serializers
from webAPI.models.cart import Cart
from webAPI.models.product import Product
from django.contrib.auth.models import User

class cartSerializers(serializers.ModelSerializer):    
    class Meta:
        model = Cart
        fields = ['id','product','user','quantity','total']