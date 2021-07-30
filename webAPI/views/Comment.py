from webAPI.models.Comment import Comment
from webAPI.serializers.CommentSerializer import CommentSerializer,CommentPostSerializer
from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.admin import User
from webAPI.models.product import Product
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        try:
            queryset = Comment.objects.all()
        except:
            raise NotAuthenticated()

        serializer = UserSerializer(queryset)
        return Response(serializer.data)
    def retrieve(self, request,pk=None):
        queryset = Comment.objects.all()
        print(pk)
        try:
            queryset = Comment.objects.filter(product=pk)
        except:
             return Response({  
                    "code": "Comment empty",
                    'msg': "ไม่มีคอมแม้นใดๆ",
                },status = status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self,request,*args,**kwargs):
        comment_data = request.data
        serializer = CommentPostSerializer(data=request.data)
        if serializer.is_valid():
            data={}
            try:
                    product_id = serializer.data['product']
                    products =Product.objects.get(pk=int(product_id))
                    message = serializer.data['message']
                    print(products)

            except:
                return Response({  
                        "code": "Comment fail",
                        'msg': "ไม่มีสินค้าในระบบ",
                    },status = status.HTTP_400_BAD_REQUEST)
                
            user_id=self.request.user
            user = User.objects.get(username=user_id)
            items = Comment.objects.create(product=products,user=user,message=message)
            items.save()
            data['id'] = items.id
            data['product'] = items.product.name
            data['message'] = items.message
            return Response({ 
                'msg': "บันทึกสำเร็จ", 
                "data": data,
                
                },status = status.HTTP_201_CREATED)
        else:
            return Response({  
                    "code": "COMMENT Fail",
                    'msg': "บันทึกไม่สำเร็จ",
                    "error": serializer.errors
                 },status = status.HTTP_400_BAD_REQUEST)