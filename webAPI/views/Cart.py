from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.cartSerializers import cartSerializers,CartGetItemSerializer,cartEditSerializers
from webAPI.models.cart import Cart
from webAPI.models.product import Product
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound ,ParseError,NotAuthenticated
from webAPI.custom_Response import ResponseInfo
from rest_framework import status
from django.contrib.auth.admin import User
from webAPI.paginations import CustomPagination
class cart_list(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = cartSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product','user']
    filterset_fields = ['id', 'product','user']
    ordering_fields = ['id','quantity', 'total']
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    # def get_queryset(self):
    #     queryset = Cart.objects.filter(user = self.request.user)
    #     return queryset
  
    def list(self, request):
        queryset = Cart.objects.filter(user=self.request.user)
        serializer = CartGetItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        data ={}
        if serializer.is_valid():
            try:
                product_id = serializer.data['product']
                products =Product.objects.get(pk=int(product_id))
            except:
               
                return Response({  
                    "code": "ADD_TO_CART_FAIL",
                    'msg': "???????????????????????????????????????????????????????????????",
                },status = status.HTTP_400_BAD_REQUEST)
             
            user_id=self.request.user
            user = User.objects.get(username=user_id)
            quantitys = int(serializer.data['quantity'])

            items = Cart.objects.filter(user=user,product=int(product_id)).first()
            if items:
                items.quantity += quantitys
                multiply=quantitys*products.price
                print('multiply:',multiply,'=',items.quantity,'*',products.price)
                items.total += multiply
                print('sum:',items.total,'=',items.total,'+',multiply)
                # print(items.user)
                items.save()   
            else:  
                items = Cart.objects.create(product=products,user=user,quantity=quantitys,total=quantitys*products.price)
                items.save()

            data['id'] = items.id
            data['product'] = items.product.name
            data['price']= items.product.price
            data['quantity'] = items.quantity
            data['total'] = items.total
            return Response({ 
                'msg': "????????????????????????????????????", 
                "data": data,
                
                },status = status.HTTP_201_CREATED)
        else:
            return Response({  
               
                "code": "ADD_TO_CART_FAIL",
                'msg': "?????????????????????????????????????????????",
                 "error": serializer.errors
                },status = status.HTTP_400_BAD_REQUEST)
   
    # def list(self, request):
    #     try:
    #         queryset = Cart.objects.filter(user=self.request.user)
    #     except:
    #         raise NotAuthenticated()

    #     serializer = CartGetItemSerializer(queryset)
    #     return Response(serializer.data)
            
    # def __init__(self, **kwargs):
    #     self.response_format = ResponseInfo().response
    #     super(cart_list, self).__init__(**kwargs)
    
    # def get(self, request, *args, **kwargs):
    #     response_data = Cart.objects.filter(user=self.request.user)
    #     serializer = cartSerializers(response_data)
    #     self.response_format["data"] = serializer.data
    #     self.response_format["status"] = True
    #     # print('response_format=',self.response_format)
    #     if not response_data:
    #         self.response_format["message"] = "List empty"
    #     return Response(self.response_format)
class cart_edit_delete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = cartSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product','user']
    filterset_fields = ['id', 'product','user']
    ordering_fields = ['id','quantity', 'total']
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # print(kwargs)
        current_user = self.request.user 
        try:
            instance = self.get_object()
            cart_user = Cart.objects.get(pk=kwargs['pk']).user
        except:
            #not found
            raise NotFound()
        #User Forbidden
        if  cart_user != current_user:
            return Response({"code": "HTTP_403_FORBIDDEN",'msg':'????????????????????????????????????????????????????????????'},status=status.HTTP_403_FORBIDDEN)
       #Delete
        self.perform_destroy(instance)
        return Response({'msg':'??????????????????????????????????????????'},status=status.HTTP_200_OK)

    def patch(self, request, pk):
        try:
          
            cartlist = Cart.objects.get(id=pk)
        except:
            raise NotFound()
        data = request.data     
        if int(data['quantity']) == 0:
            cartlist.delete()
            return Response({
                "msg":"??????????????????????????????????????????",
            },200)
        if int(data['quantity']) < 0:
            return Response({
                "msg":"??????????????????????????????????????????????????????",
            },400)
        
        cartlist.total = int(data['quantity'])*(cartlist.product.price)
        cartlist.quantity = data['quantity']
        cartlist.save()
        response = cartSerializers(cartlist).data
        return Response({
            "msg" : "????????????????????????????????????",
            "data":[response]
        })
  
    def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            if serializer.data:
                custom_data = {
                        "status": "?????????????????????????????????????????????",
                        "data": serializer.data
                }
                return Response(custom_data)

   
