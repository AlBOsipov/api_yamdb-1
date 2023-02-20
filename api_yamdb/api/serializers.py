from rest_framework import serializers
from reviews.models import Review, Comment, Title, Category, Genre, GenreTitle


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
