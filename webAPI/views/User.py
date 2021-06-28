from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics

#serializer & Models
from webAPI.serializers.userSerializers import UserSerializer,GroupSerializer,RegisterApiSerializer
from django.contrib.auth.models import User,Group
#viewSET
from rest_framework import viewsets
#permission & Authenticated
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
#api_root
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers
#token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings 

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'group':reverse('group',request=request, format=format),
        'product': reverse('product-list', request=request, format=format),
        'product_image': reverse('product_image-list', request=request, format=format),
        'category': reverse('category-list',request=request, format=format),
        'cart': reverse('cart-list',request=request, format=format),
        'invoice': reverse('invoice-list',request=request, format=format),
        'invoice_item': reverse('invoice_item-list',request=request, format=format),
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly,]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly,]

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterApiSerializer
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #auto token
        # token, created = Token.objects.get_or_create(user=serializer.instance)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
            # 'token': token.key, 
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            # 'token_type':token_type,
        })
   