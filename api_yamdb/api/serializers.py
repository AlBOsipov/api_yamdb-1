from rest_framework import serializers
from reviews.models import YaMdbUser


from rest_framework import serializers

from reviews.models import YaMdbUser


# Эндпоинт /singup/
class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = YaMdbUser
        fields = ('email', 'username')

# Эндпоинт /users/me/
class SelfUserPageSerializer(serializers.ModelSerializer):
    """Сериализатор своей страницы."""
    username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = YaMdbUser
