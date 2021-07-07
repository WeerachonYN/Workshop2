from rest_framework import serializers
from webAPI.models.Invoice import invoice
from webAPI.serializers.Invoice_itemSerializer import Invoice_ItemSerializers
#list
class InvoiceSerializers(serializers.ModelSerializer):
    # invoices_item = serializers.HyperlinkedRelatedField(many=True, view_name='invoices-detail', read_only=True)
    
    class Meta:
        model = invoice
        fields = ['url','id','user','created_datetime','updated_datetime','total','status']
# detail
class InvoiceDetailSerializers(serializers.ModelSerializer):
    invoices_item = Invoice_ItemSerializers(many=True,  read_only=True)
    # invoices_item = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='invoice-item')
    
    class Meta:
        model = invoice
        fields = ['id','user','created_datetime','updated_datetime','total','invoices_item']
#check_out
class checkoutSerializers(serializers.ModelSerializer):
    class Meta:
        model = invoice
        fields = ['id']
