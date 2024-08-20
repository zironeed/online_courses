from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription
from users.models import Balance

User = get_user_model()


class BalanceSerializer(serializers.ModelSerializer):
    """Баланс пользователя"""

    class Meta:
        model = Balance
        fields = '__all__'

class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    # TODO

    class Meta:
        model = Subscription
        fields = '_all__'
