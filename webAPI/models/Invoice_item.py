from django.db import models
from webAPI.models.product import Product
from webAPI.models.Invoice import invoice
import datetime

class invoice_item(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE,related_name='invoices_product',default=None,null=True)
    invoice = models.ForeignKey(invoice, on_delete = models.CASCADE,related_name='invoices_item',default=None,null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=7, decimal_places=3 )

    def __str__(self):
        return self.product.name