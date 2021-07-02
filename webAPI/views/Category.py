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
from webAPI.exception import custom_exception_handler
from rest_framework.exceptions import NotFound
class category_list(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = categorySerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'name']
    filterset_fields = ['is_enabled']
    ordering_fields = ['id','name']
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

   



    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     if self.check_signin_details(self.request.data):
    #         self.perform_create(serializer)
    #         return Response(data={"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    #     return Response(data={"message": "Password or username policy failed."}, status=status.HTTP_400_BAD_REQUEST)
    

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
           
             
        
    