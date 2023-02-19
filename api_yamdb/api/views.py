from reviews.models import Review, Title, Genre, Category
from rest_framework import viewsets
from api.serializers import (ReviewSerializer, CommentSerializer,
                             TitleSerialzier, GenreSerializer,
                             CategorySerializer)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями произведений"""

    serializer_class = TitleSerialzier
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями жанров"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )


class CategoriesViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями категорий"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        '''Функция возвращения всех комментариев поста.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        '''Функция создания нового комментария к посту.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user,
                        title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        '''Функция возвращения всех комментариев поста.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id),
            pk=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        '''Функция создания нового комментария к посту.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id),
            pk=review_id
        )
        serializer.save(author=self.request.user,
                        review=review)
