from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer,TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,AuthenticationFailed,ParseError
from django.contrib.auth import password_validation
from webAPI.serializers.UserImage import ImageUserSerializer
from rest_framework.validators import UniqueValidator

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    # users = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    images = ImageUserSerializer()
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name','email','images']

class UserEditSerializer(serializers.ModelSerializer):
    email = email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    images = ImageUserSerializer()
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name','email','images']
    def validate_email(email):
        if email.is_valid() :
            raise serializers.ValidationError('กรุณากรอกอีเมล์ให้ถูกต้อง.')
#loginTOKEN
class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            # user = {
            #     id:
            # }
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            data['expires_in'] = int(refresh.access_token.lifetime.total_seconds())
            data['token_type']= str(refresh.token_type)
            return data
        except:            
            raise ParseError({
                "msg" : "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
                "code": "LOGIN_FAIL"
                }, 400)
        return super().validate(attrs)


#registerTOKEN
class RegisterApiSerializer(serializers.ModelSerializer):
    
    # username = serializers.CharField(max_length=10,error_messages={"blank": "กรุณากรอกชื่อผู้ใช้งาน"})
    # password = serializers.CharField(max_length=10,error_messages={"blank": "กรุณากรอกรหัสผ่าน"})
    class Meta:
        model = User
        fields = ['id','username','password','first_name', 'last_name']
        extra_kwargs = {'password':{'write_only': True},'username':{'write_only': True}}

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError('รหัสผ่านต้องมากกว่า 8 ตัวอักษร')
        return password

    def create(self, validated_data):
        user = User.objects.create_user(
           username= validated_data['username'],     
            password = validated_data['password']  ,
            first_name=validated_data['first_name'],  
            last_name=validated_data['last_name'])
        
        user.save()
        return user

#refreshTOKEN
class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            refresh = RefreshToken(attrs['refresh'])
            data['refresh']= str(refresh)
            data['token_type']= str(refresh.token_type)
            data['expires_in'] = int(refresh.access_token.lifetime.total_seconds())
            return data
        except:

            raise AuthenticationFailed({
                "msg" : "Refetch Token ไม่ถูกต้อง",
                "code": "REFETCH_TOKEN_FAIL"
                }, 401)
        return super().validate(attrs)
   