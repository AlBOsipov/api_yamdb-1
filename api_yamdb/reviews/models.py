from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User():
    pass

class Title():
    pass


class Review(models.Model):
    """Модель для отзывов к произведениям."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    # В условии: На одно произведение - один отзыв от автора.
    # Я сначала хотела здесь применить OneToOneField. Но это бы дало, наверно, что у одного произведения будет один отзыв.
    # Так что скорее всего это условие учитывается в модели Title.
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'    

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для комментариев к отзывам."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'    

    def __str__(self):
        return self.text
