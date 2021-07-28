from webAPI.models.Comment import Comment
from rest_framework import serializers
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'name','message','product','user','datetime','is_activate']
   