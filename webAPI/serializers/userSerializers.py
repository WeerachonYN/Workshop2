from django.contrib.auth.models import User,Group
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    # users = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name','email']

class RegisterApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password','email','first_name', 'last_name']
        extra_kwargs = {'password':{'write_only': True},}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],   email=validated_data['email'],  password = validated_data['password']  ,first_name=validated_data['first_name'],  last_name=validated_data['last_name'])
        # token = super().get_token(user)
        # token['name'] = user.name
        return user

class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['refresh']= str(refresh)
        data['token_type']= str(refresh.token_type)
        data['expires_in'] = int(refresh.access_token.lifetime.total_seconds())
        return data