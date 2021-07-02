from rest_framework import serializers
from webAPI.models.cart import Cart
from webAPI.models.product import Product
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
class cartSerializers(serializers.ModelSerializer):    
    product = serializers.CharField(max_length=20,
            error_messages={"blank": "กรุณากรอกรหัสสินค้า",'write_only':True})

    quantity = serializers.IntegerField(
             error_messages={"blank": "กรุณาใส่จำนวนสินค้า",'write_only':True})

    class Meta:
        model = Cart
        fields = ['id','product','user','quantity','total']
        extra_kwargs = {'quantity':{'write_only': True}}

    def validate_quantity(self, quantity):
        if quantity < 1:
            raise ValidationError('จำนวนสินค้าต้องมากกว่า 0 ชิ้น')
        return quantity
        

    def validate_product(self, product):
        try:
            is_enableds = Product.objects.get(pk = int(product))
        except:
             raise ValidationError('ไม่พบสินค้า')
        
        if not is_enableds.is_enabled:
            raise ValidationError('สินค้านี้ถูกปิดการใช้งาน')
        return product
        
class cartEditSerializers(serializers.ModelSerializer):    
    # product = serializers.CharField(max_length=20,
    #         error_messages={"blank": "กรุณากรอกรหัสสินค้า",'write_only':True})

    quantity = serializers.IntegerField(
             error_messages={"blank": "กรุณาใส่จำนวนสินค้า",'write_only':True})

    class Meta:
        model = Cart
        fields = ['id','user','quantity','total']
        extra_kwargs = {'quantity':{'write_only': True}}