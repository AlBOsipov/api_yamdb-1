from rest_framework import serializers
from reviews.models import Review, Comment


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
