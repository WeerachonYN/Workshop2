from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#serializer & Models
from webAPI.serializers.Invoice_itemSerializer import Invoice_ItemSerializers
from webAPI.models.Invoice_item import invoice_item
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class invoice_item_list(generics.ListCreateAPIView):
    queryset = invoice_item.objects.all()
    serializer_class = Invoice_ItemSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id','product','invoice']
    filterset_fields = ['id', 'created_datetime','product']
    ordering_fields = ['id','created_datetime', 'quantity']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        data ={}
        # if serializer.is_valid():
        #     try:
        #         # product_id = serializer.data['product']
        #         # products =Product.objects.get(pk=int(product_id))
        #         cartItem = Cart.objects.filter
        #     except:
        #         return Response({  
        #             "code": "ADD_TO_CART_FAIL",
        #             'msg': "สินค้าไม่มีตามที่ระบุ",
        #         },status = status.HTTP_400_BAD_REQUEST)
             
        #     user_id=self.request.user
        #     user = User.objects.get(username=user_id)
        #     # print('user=',self.request.user)
        #     quantitys = int(serializer.data['quantity'])
        #     items = Cart.objects.filter(user=user,product=int(product_id)).first()
        #     if items:
        #         items.quantity += quantitys
        #         multiply=quantitys*products.price
        #         print('multiply:',multiply,'=',items.quantity,'*',products.price)
        #         items.total += multiply
        #         print('sum:',items.total,'=',items.total,'+',multiply)
        #         # print(items.user)
        #         items.save()   
        #     else:  
        #         new_item = Cart.objects.create(product=products,user=user,quantity=quantitys,total=quantitys*products.price)
        #         new_item.save()

        #     data['id'] = items.id
        #     data['product'] = items.product.name
        #     data['quantity'] = items.quantity
        #     data['total'] = items.total
        #     return Response({ 
        #         'msg': "บันทึกสำเร็จ", 
        #         "data": data,
                
        #         },status = status.HTTP_201_CREATED)
        # else:
        #     return Response({  
               
        #         "code": "ADD_TO_CART_FAIL",
        #         'msg': "บันทึกไม่สำเร็จ",
        #          "error": serializer.errors
        #         },status = status.HTTP_401_UNAUTHORIZED)
   
class invoice_item_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = invoice_item.objects.all()
    serializer_class = Invoice_ItemSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                