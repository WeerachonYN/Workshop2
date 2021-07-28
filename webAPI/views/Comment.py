from webAPI.models.Comment import Comment
from webAPI.serializers.CommentSerializer import CommentSerializer
from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
class CommentViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = Comment.objects.get(user=self.request.user)
        except:
            raise NotAuthenticated()

        serializer = CommentSerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(user)
        return Response(serializer.data)
