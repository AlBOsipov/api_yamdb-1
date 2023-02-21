from rest_framework import serializers
from reviews.models import YaMdbUser
from rest_framework.exceptions import ValidationError
from reviews.models import Review, Comment, Title, Category, Genre, GenreTitle
from rest_framework.response import Response
from rest_framework import status


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Category"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Genre"""

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerialzier(serializers.ModelSerializer):
    """Сериализатор для объекта класса Title"""

    genres = GenreSerializer(many=True)
    category = CategorySerializer()

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        category = validated_data.pop('category')
        current_category, status = Category.objects.get_or_create(**category)
        validated_data['category'] = current_category
        title = Title.objects.create(**validated_data)

        for genre in genres:
            current_genres, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genres, title=title)
        return title

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'category', 'genres')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Review."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        """Валидация на уже существующий отзыв к произведению
        от одного автора."""
        review1 = Review.objects.filter(
            author=self.context('request').user,
            title=self.context('view').kwargs('title_id')
        ).exists()
        if self.context.get('request').method == 'POST' and review1:
            raise serializers.ValidationError(
                'На одно произведение можно оставить только один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса Comment."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(
        read_only=True)
    review = serializers.PrimaryKeyRelatedField(
        read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


# Эндпоинт /singup/
class UserSingUpSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса регистрации."""

    class Meta(object):
        model = YaMdbUser
        fields = ('email', 'username',)

    def validate(self, data):
        username = data['username']
        email = data['email']
        if YaMdbUser.objects.filter(username=username).exists():
            user = YaMdbUser.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError('Пользователь с таким username уже существует, но email не соответствует')
            else:
                confirmation_code = self.generat_conf_code(user)
                self.send_code_on_email(user, confirmation_code)
                raise serializers.ValidationError('Код подтверждения отправлен на почту.')
        return data

# Эндпоинт /user/
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = YaMdbUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


# Эндпоинт /users/me/
class SelfUserPageSerializer(serializers.ModelSerializer):
    """Сериализатор своей страницы."""
    last_name = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = YaMdbUser
        read_only_fields = ('role',)


# Эндпоинт /token/
class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,)
    confirmation_code = serializers.CharField(max_length=50,)
