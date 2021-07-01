from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

#serializer & Models
from webAPI.serializers.userSerializers import UserSerializer,GroupSerializer,RegisterApiSerializer
from django.contrib.auth.models import User,Group
#viewSET
from rest_framework import viewsets
#filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
#permission & Authenticated
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
#api_root
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers
#token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings 
#datetime
import datetime,jwt
#exception
from webAPI.exception import custom_exception_handler
#jwt
from rest_framework_simplejwt.views import TokenViewBase
from webAPI.serializers.userSerializers import TokenRefreshLifetimeSerializer,TokenObtainLifetimeSerializer
from rest_framework import status

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register':reverse('register', request=request, format=format),
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
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['id', 'username','email']
    filterset_fields = ['id', 'is_active','is_staff']
    ordering_fields = ['id','username', 'date_joined']
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

#Register
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterApiSerializer
    permission_classes = (AllowAny, )
    
    def post(self, request, *args,  **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.save()
            #auto token
            # token, created = Token.objects.get_or_create(user=serializer.instance)
            refresh = RefreshToken.for_user(user)
            return Response({
                # "user": UserSerializer(user,    context=self.get_serializer_context()).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'token_type':str(refresh.token_type),
                'expires_in':int(refresh.access_token.lifetime.total_seconds()),

                },status = status.HTTP_201_CREATED)
        else:
            # error_list = [serializer.errors[error][0] for error in serializer.errors]
            return Response({
                 "msg" : "ลงทะเบียนไม่สำเร็จ",
                 "code": "REGISTER_FAIL",
                 "errors":serializer.errors,
               
            },status = status.HTTP_400_BAD_REQUEST)
#LOGIN
class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = TokenObtainLifetimeSerializer
#REFESH
class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """
    serializer_class = TokenRefreshLifetimeSerializer