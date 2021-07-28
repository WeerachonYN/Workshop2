from rest_framework import serializers
from webAPI.models.Invoice_item import invoice_item
from webAPI.serializers.productSerializer import Product_CARTSerializers
class Invoice_ItemSerializers(serializers.ModelSerializer):
    product = Product_CARTSerializers()
    class Meta:
        model = invoice_item
        fields = ['id','invoice','created_datetime','quantity','total','product']