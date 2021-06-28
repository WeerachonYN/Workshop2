from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#serializer & Models
from webAPI.serializers.InvoiceSerializers import InvoiceSerializers
from webAPI.models.Invoice import invoice
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class invoice_list(generics.ListCreateAPIView):
    queryset = invoice.objects.all()
    serializer_class = InvoiceSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class invoice_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = invoice.objects.all()
    serializer_class = InvoiceSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                