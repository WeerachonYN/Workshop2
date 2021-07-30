from webAPI.models.Comment import Comment
from rest_framework import serializers
from webAPI.serializers.userSerializers import UserSerializer
from rest_framework.exceptions import ValidationError
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ['id','user', 'message','product','datetime','is_activate']
class CommentPostSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Comment
        fields = ['message','product','user']
