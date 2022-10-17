from rest_framework import serializers
from reviews.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для запроса кода подтверждения"""
    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериалайзер для запроса токена."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=255, required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с пользователями."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class UserPatchMeSerializer(UserSerializer):
    """Сериализатор для работы со своим профилем."""
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
