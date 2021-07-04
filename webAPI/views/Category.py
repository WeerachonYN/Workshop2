from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
from django.http import request
from django.conf import settings
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.categorySerializers import categorySerializers
from webAPI.models.category import Category
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from webAPI.paginations import CustomPagination
from webAPI.ordering import MyCustomOrdering
from rest_framework.exceptions import NotFound
from webAPI.custom_Response import ResponseInfo
class category_list(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = categorySerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'name']
    filterset_fields = ['is_enabled']
    ordering_fields = ['id','name']
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(category_list, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        response_data = super(category_list, self).list(request, *args, **kwargs)
        self.response_format["data"] = response_data.data
        self.response_format["status"] = True
        if not response_data.data:
            self.response_format["message"] = "List empty"
        return Response(self.response_format)
class category_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = categorySerializers
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
           
             
        
    