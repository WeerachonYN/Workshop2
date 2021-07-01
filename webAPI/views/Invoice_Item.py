from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#serializer & Models
from webAPI.serializers.Invoice_itemSerializer import Invoice_ItemSerializers
from webAPI.models.Invoice_item import invoice_item
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class invoice_item_list(generics.ListCreateAPIView):
    queryset = invoice_item.objects.all()
    serializer_class = Invoice_ItemSerializers
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id','product','invoice']
    filterset_fields = ['id', 'created_datetime','product']
    ordering_fields = ['id','created_datetime', 'quantity']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class invoice_item_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = invoice_item.objects.all()
    serializer_class = Invoice_ItemSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                