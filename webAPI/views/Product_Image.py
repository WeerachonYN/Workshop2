from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.productImageSerializers import ProductImageSerializers
from webAPI.models.productImage import ProductImage
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class product_Image_list(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product']
    filterset_fields = ['id', 'product']
    ordering_fields = ['id']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        data ={}
        if serializer.is_valid():
            try:
                # product_id = serializer.data['product']
                products =Product.objects.get(pk=int(product_id))
            except:
                # print('เราจะตายกันหมด!')
                return Response({  
                    "code": "ADD_TO_CART_FAIL",
                    'msg': "สินค้าไม่มีตามที่ระบุ",
                },status = status.HTTP_400_BAD_REQUEST)
             
            user_id=self.request.user
            user = User.objects.get(username=user_id)
            # print('user=',self.request.user)
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
                new_item = Cart.objects.create(product=products,user=user,quantity=quantitys,total=quantitys*products.price)
                new_item.save()

            data['id'] = items.id
            data['product'] = items.product.name
            data['quantity'] = items.quantity
            data['total'] = items.total
            return Response({ 
                'msg': "บันทึกสำเร็จ", 
                "data": data,
                
                },status = status.HTTP_201_CREATED)
        else:
            return Response({  
               
                "code": "ADD_TO_CART_FAIL",
                'msg': "บันทึกไม่สำเร็จ",
                 "error": serializer.errors
                },status = status.HTTP_401_UNAUTHORIZED)
   
class product_Image_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                