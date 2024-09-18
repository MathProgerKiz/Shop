from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from users.api.serializers import UserSerializers
from users.models import User
from users.permissions import IsAdminOrReadOnly


@extend_schema(tags=['User'])
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]
