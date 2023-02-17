from django.shortcuts import render
from reviews.models import Review, Title
from rest_framework import viewsets
from api.serializers import ReviewSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
