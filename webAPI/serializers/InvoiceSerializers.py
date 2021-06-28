from rest_framework import serializers
from webAPI.models.Invoice import invoice

class InvoiceSerializers(serializers.ModelSerializer):
    invoices_item = serializers.HyperlinkedRelatedField(many=True, view_name='invoice_item-detail', read_only=True)
    class Meta:
        model = invoice
        fields = ['id','user','created_datetime','updated_datetime','total','status','invoices_item']