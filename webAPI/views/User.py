from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

#serializer & Models
from webAPI.serializers.userSerializers import UserSerializer,GroupSerializer,RegisterApiSerializer,UserEditSerializer
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
from rest_framework.exceptions import NotAuthenticated,NotFound,ParseError
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'register':reverse('register', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'ImageUser':reverse('imageUser-list',request=request, format=format),
        'comment':reverse('comment-list',request=request, format=format),
        'group':reverse('group',request=request, format=format),
        'product': reverse('product-list', request=request, format=format),
        'category': reverse('category-list',request=request, format=format),
        'cart': reverse('cart-list',request=request, format=format),
        'invoice': reverse('invoice-list',request=request, format=format),
    
    })

class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = User.objects.get(username=self.request.user)
        except:
            raise NotAuthenticated()

        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def patch(self, request, pk=None):
        try:
            userlist = User.objects.get(id=pk)
        except:
            raise NotFound()
        data = request.data     
        if data['email'] is not None:
            userlist.first_name = data['first_name']
            userlist.last_name = data['last_name']
            userlist.email = data['email']
            userlist.save()
            response = UserEditSerializer(userlist).data
            return Response({
                "msg" : "บันทึกสำเร็จ",
                "data":[response]
            })
        return Response({
             "code" : "บันทึกไม่สำเร็จ",
             "msg":validate_email.error
        },400)

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
        serializer = RegisterApiSerializer(data=request.data)
        data ={}
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data['refresh'] = str(refresh)
            data['access']=str(refresh.access_token)
            data['token_type']=str(refresh.token_type)
            data['expires_in']=int(refresh.access_token.lifetime.total_seconds())
            return Response(data,status = status.HTTP_201_CREATED)
        else:
            # error_list = [serializer.errors[error][0] for error in serializer.errors]
            data = serializer.errors
            return Response({
                 "msg" : "ลงทะเบียนไม่สำเร็จ",
                 "code": "REGISTER_FAIL",
                 "errors":data,
               
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

# class EditUserSerializers(serializers.ModelSerializer):    
#     first_name = serializers.CharField(max_length=20,
#             error_messages={"blank": "กรุณากรอกชื่อ",'write_only':True})

#     last_name = serializers.IntegerField(
#              error_messages={"blank": "กรุณากรอกนามสกุล",'write_only':True})
#     email = serializers.CharField(
#              error_messages={"blank": "กรุณากรอกอีเมล์",'write_only':True})
    
#     class Meta:
#         model = User
#         fields = ['id','username','first_name','last_name','email']
#         extra_kwargs = {'username':{'write_only': True}}

  
#     def validate_product(self, product):
#         try:
#             is_enableds = Product.objects.get(pk = int(product))
#         except:
#              raise ValidationError('ไม่พบสินค้า')
        
#         if not is_enableds.is_enabled:
#             raise ValidationError('สินค้านี้ถูกปิดการใช้งาน')
#         return product