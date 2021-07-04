from rest_framework import serializers
from webAPI.models.Invoice_item import invoice_item

class Invoice_ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = invoice_item
        fields = ['id','product','invoice','created_datetime','quantity','total']