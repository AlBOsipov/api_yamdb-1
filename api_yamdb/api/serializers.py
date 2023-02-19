from rest_framework import serializers
from reviews.models import YaMdbUser


from rest_framework import serializers

from reviews.models import YaMdbUser


# Эндпоинт /singup/
class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = YaMdbUser
        fields = ('email', 'username', 'confirmation_code')

# Эндпоинт /users/me/
class SelfUserPageSerializer(serializers.ModelSerializer):
    """Сериализатор своей страницы."""
    username = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = YaMdbUser

# Эндпоинт /token/
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        code = attrs.get('confirmation_code')
        if username and code:
            try:
                user = YaMdbUser.objects.get(username=username, code=code)
            except YaMdbUser.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Username and code are required')
        attrs['user'] = user
        return attrs