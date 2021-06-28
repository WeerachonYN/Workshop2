from django.shortcuts import render,redirect
from rest_framework.response import Response
from rest_framework import generics
#serializer & Models
from webAPI.serializers.categorySerializers import categorySerializers
from webAPI.models.category import Category
#permission & Authenticated
from rest_framework import permissions
from webAPI.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class category_list(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = categorySerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

class category_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = categorySerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
                