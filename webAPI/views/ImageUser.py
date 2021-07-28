from webAPI.models.ImageUser import ImageUser
from webAPI.serializers.UserImage import ImageUserSerializer
from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
class ImageUserViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            queryset = ImageUser.objects.get(user=self.request.user)
        except:
            raise NotAuthenticated()

        serializer = ImageUserSerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = ImageUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ImageUserSerializer(user)
        return Response(serializer.data)
