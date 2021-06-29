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
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class product_Image_list(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product']
    filterset_fields = ['id', 'product']
    ordering_fields = ['id']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class product_Image_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                