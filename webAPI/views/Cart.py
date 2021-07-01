from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.cartSerializers import cartSerializers
from webAPI.models.cart import Cart
from webAPI.models.product import Product
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound ,NotAuthenticated
from webAPI.custom_Response import ResponseInfo
from rest_framework import status
from django.contrib.auth.admin import User

class cart_list(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = cartSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product','user']
    filterset_fields = ['id', 'product','user']
    ordering_fields = ['id','quantity', 'total']
    permission_classes = [permissions.IsAuthenticated]
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)  
   
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        print('req_data=',request.data)
        if serializer.is_valid():
            user_id=self.request.user
            user = User.objects.get(username=user_id)
            print(user)
            product_id = serializer.data['product']
            products =Product.objects.get(pk=int(product_id))
            quantitys = serializer.data['quantity']
            items = Cart.objects.filter(user=user,product=int(product_id)).first()
            
            if items:
                    #เพิ่ม 
                items.quantity += quantitys
                    
                multiply=quantitys*products.price
                print('multiply:',multiply,'=',items.quantity,'*',products.price)
                items.total += multiply
                print('sum:',items.total,'=',items.total,'+',multiply)
                # print(items.user)
                items.save()   
            else:
                    
                new_item = Cart.objects.create(product=products,user=user,quantity=quantitys,total=quantitys*products.price)
                new_item.save()
                # serializer = CartSerializer(self.get_object())
            return Response({  
                "data": serializer.data,

                'msg': "บันทึกสำเร็จ"
                
                },status = status.HTTP_201_CREATED)
        else:
            raise NotAuthenticated("บันทึกไม่สำเร็จ")
        
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(cart_list, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        response_data = super(cart_list, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = True
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)

        
        
class cart_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = cartSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product','user']
    filterset_fields = ['id', 'product','user']
    ordering_fields = ['id','quantity', 'total']
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user=self.request.user
            product_id = serializer.data['product']
            products =Product.objects.get(pk=int(product_id))
            quantitys = serializer.data['quantity']
            items = Cart.objects.filter(user=user,product=int(product_id)).first()
            
            if items.quantity ==1:
                items.delete()
            else:
                    #เพิ่ม
                items.quantity -= quantitys
                    
                multiply=quantitys*products.price
                print('multiply:',multiply,'=',items.quantity,'*',products.price)
                items.total -= multiply
                print('sum:',items.total,'=',items.total,'+',multiply)
                    # print(items.quantity)
                items.save()   
                # serializer = CartSerializer(self.get_object())
            return Response({  
                "data": serializer.data,

                'msg': "ลบสำเร็จ"
                
                },status = status.HTTP_201_CREATED)
        else:
            raise NotAuthenticated("ลบไม่สำเร็จ",e)

    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            if serializer.data:
                custom_data = {
                        "status": "ดึงข้อมูลสำเร็จ",
                        "data": serializer.data
                }
                return Response(custom_data)
    def perform_update(self, serializer):
        instance = serializer.save()
        send_email_confirmation(user=self.request.user, modified=instance)
    # def partial_update(self, request,**kwargs):
        
    #     try:
    #         queryset = Cart.objects.get(pk=kwargs)
    #     except queryset.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     serializer = cartSerializers(queryset,data=request.data)
    #     data= {}
    #     if serializer.is_valid():
    #         serializer.save()
    #         data['success'] = "update successful"
    #         return Response(data=data)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
  