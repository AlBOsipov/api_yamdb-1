from rest_framework import serializers
from reviews.models import YaMdbUser


from rest_framework import serializers

from reviews.models import YaMdbUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from reviews.models import YaMdbUser

# Эндпоинт /singup/
class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = YaMdbUser
        fields = ('email', 'username', 'confirmation_code')

# Эндпоинт /users/me/
class SelfUserPageSerializer(serializers.ModelSerializer):
    """Сериализатор своей страницы."""

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = YaMdbUser

# Эндпоинт /token/
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()