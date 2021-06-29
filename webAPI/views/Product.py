from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.productSerializer import ProductSerializers
from webAPI.models.product import Product
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
#custom pagination
from webAPI.paginations import CustomPagination
class product_list(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['name']
    filterset_fields = ['id', 'is_enabled','price']
    ordering_fields = ['price','created_datetime']

    pagination_class = CustomPagination
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        sort_by = self.request.query_params.get('sort','desc')
        #get params
        category_in = self.request.query_params.get('category__in',None)
        list_params =[]
        #params to list
        if category_in is not None:
            for cate_in in category_in.split('|'):
                list_params.append(int(cate_in))
        #sort
        if sort_by == 'desc':
            queryset = queryset.order_by('price')
        else:
            queryset = queryset.order_by('-price')
        #filter 
        if category_in is not None:
            queryset = queryset.filter(category__in=list_params)
        return queryset
        
       

class product_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                