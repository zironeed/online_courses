from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from product.custom_permissions import IsStaff
from api.v1.serializers.user_serializer import CustomUserSerializer, BalanceSerializer
from product.users.models import Balance

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["get", "head", "options"]
    permission_classes = (permissions.IsAdminUser,)


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    http_method_names = ['put', 'patch']
    permission_classes = (IsStaff, )
