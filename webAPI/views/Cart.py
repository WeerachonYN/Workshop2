from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#serializer & Models
from webAPI.serializers.cartSerializers import cartSerializers
from webAPI.models.cart import Cart
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class cart_list(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = cartSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product','user']
    filterset_fields = ['id', 'product','user']
    ordering_fields = ['id','quantity', 'total']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class cart_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = cartSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'product','user']
    filterset_fields = ['id', 'product','user']
    ordering_fields = ['id','quantity', 'total']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                