from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#serializer & Models
from webAPI.serializers.productSerializer import ProductSerializers
from webAPI.models.product import Product
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class product_list(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class product_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                