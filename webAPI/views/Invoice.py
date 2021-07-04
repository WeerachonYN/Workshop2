from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.InvoiceSerializers import InvoiceSerializers,checkoutSerializers,InvoiceDetailSerializers
from webAPI.models.Invoice import invoice
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from webAPI.models.cart import Cart
from webAPI.models.Invoice_item import invoice_item
import datetime
from rest_framework.exceptions import NotFound
from rest_framework import status
from webAPI.custom_Response import ResponseInfo

class invoice_list(generics.ListAPIView):
    queryset = invoice.objects.all()
    serializer_class = InvoiceSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'user','status']
    filterset_fields = ['created_datetime', 'status','user']
    ordering_fields = ['id','created_datetime', 'status']
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(invoice_list, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        response_data = super(invoice_list, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = True
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)
        
    
class invoice_detail(generics.RetrieveAPIView):
    queryset = invoice.objects.all()
    serializer_class = InvoiceDetailSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'user','status']
    filterset_fields = ['created_datetime', 'status','user']
    ordering_fields = ['id','created_datetime', 'status']
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if serializer.data:
            custom_data = {
                    "status": "ดึงข้อมูลสำเร็จ",
                    "data": serializer.data
            }
            return Response(custom_data)

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj =  queryset.get(pk=self.kwargs['pk'])
            
        except:
            raise NotFound()
        return obj          

class checkouts(generics.CreateAPIView):
    queryset = invoice.objects.all()
    serializer_class = checkoutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data ={}
        carts = Cart.objects.filter(user=self.request.user) 
        sum_total=0
        print(len(carts))
        if len(carts)!=0:
            for i in carts:
            
                if not i.product.is_enabled:
                    return Response({
                "code": "CHECKOUT_FAIL",
                "msg": "มีสินค้าบางรายการไม่สามารถสั่งซื้อได้",
                },status=status.HTTP_400_BAD_REQUEST)
                else:
                    sum_total += i.total
            
            invoices = invoice.objects.create(user=self.request.user,total=sum_total)
            print(invoices)
            if invoices:
                invoices.save()
                for item in carts:
                    invoice_items = invoice_item.objects.create(product=item.product,invoice=invoices,quantity=item.quantity,total=item.total)
                    if invoice_items:
                        invoice_items.save()
                        item.delete()
            else:
                return Response({
                "msg":"ไม่มีใบสั่งซื้อสินค้า",
                "code": "CHECKOUT_FAIL",
            },status=status.HTTP_400_BAD_REQUEST)
            data['id']=invoices.id
            return Response({
                "msg":"สร้างรายการสั่งซื้อสำเร็จ",
                "id": data
            },status=200)
        else:
            return Response({
            "code": "CART_EMPTY",
            "msg": "กรุณาเลือกสินค้าใส่ตะกร้า",
            },status=status.HTTP_400_BAD_REQUEST)

class void_status(generics.CreateAPIView):
    queryset = invoice.objects.all()
    serializer_class = InvoiceSerializers()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            invoices = invoice.objects.get(id=pk)
        except:
            raise NotFound()
        # data = request.data
        if invoices.status == "Success":
            return Response({
                "code": "VOID_INVOICE_FAIL",
                "msg": "ยกเลิกรายการไม่สำเร็จเนื่องจากอยู่ในสถานะ ชำระเงินแล้ว"
            },status=status.HTTP_400_BAD_REQUEST)
        if invoices.status == "Cancel":
            return Response({
                "code": "VOIDED",
                "msg": "รายการสินค้านี้อยู่ในสถานะ 'ยกเลิก' รายการแล้ว"
            },status=status.HTTP_400_BAD_REQUEST)
        invoices.status = "Cancel"
        invoices.save()
        return Response({
            "msg" : "ยกเลิกรายการสำเร็จ",
        },status=status.HTTP_200_OK)
  