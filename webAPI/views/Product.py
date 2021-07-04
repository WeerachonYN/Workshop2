from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.productSerializer import Product_ListSerializers,Product_DetailSerializers
from webAPI.models.product import Product
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from webAPI.custom_Response import ResponseInfo
#custom pagination

from webAPI.paginations import CustomPagination

class product_list(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = Product_ListSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['id', 'is_enabled','price']
    ordering_fields = ['price','created_datetime']
    pagination_class = CustomPagination
    
   

    def get_queryset(self):
        queryset = Product.objects.all()
        sort_by = self.request.query_params.get('sort','desc')
        #get params
        category_in = self.request.query_params.get('category__in',None)
        category_not_in = self.request.query_params.get('category_not_in',None)

        list_params_in =[]
        list_params_not_in =[]
        #params to list in
        if category_in:
            for i in category_in.split(","):
                list_params_in.append(int(i))

        #params to list not in
        if category_not_in:
            for i in category_not_in.split(","):
                list_params_not_in.append(int(i))
        #sort
        if sort_by == 'desc':
            queryset = queryset.order_by('price','created_datetime')
        else:
            queryset = queryset.order_by('-price','-created_datetime')
        #filter in
        if category_in:
            queryset = queryset.filter(category__in=list_params_in)
        #filter not in  
        if category_not_in:
            queryset = queryset.exclude(category__in=list_params_not_in)
        
        return queryset

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(product_list, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        response_data = super(product_list, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = True
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)
        
class product_detail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = Product_DetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
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