from django.core.management.base import BaseCommand
import io
import csv
from reviews.models import (
    Genre, Category, Comment, GenreTitle, Review, YaMdbUser
)


class Command(BaseCommand):

    def genre_load(self):
        with io.open('static/data/users.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            # Только в файле не дописаны данные. Нам нужно дописать?
            for row in reader:
                user = YaMdbUser(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[4],
                    bio=row[3],
                    first_name=row[4],
                    last_name=row[5]
                )
                user.save()

    def category_load(self):
        with io.open('static/data/category.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                category = Category(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
                category.save()

    def comments_load(self):
        with io.open('static/data/comments.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                comment = Comment(
                    id=row[0],
                    review=row[1],
                    text=row[2],
                    # Тут непонятно как к автору обращаться, так как в файле указан id. Нужно тут создавать тоже юзера?
                    author=row[3],
                    pub_date=row[4]
                )
                comment.save()

    def genre_title_load(self):
        with io.open('static/data/genre_title.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                genre_title = GenreTitle(
                    id=row[0],
                    genre=row[1],
                    title=row[2],
                )
                genre_title.save()

    def review_load(self):
        with io.open('static/data/review.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                review = Review(
                    id=row[0],
                    title=row[1],
                    text=row[2],
                    # Тут непонятно как к автору обращаться
                    author=row[3],
                    score=row[4],
                    pub_date=row[5]
                )
                review.save()
    
    def users_load(self):
        with io.open('static/data/users.csv', "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                review = Review(
                    id=row[0],
                    title=row[1],
                    text=row[2],
                    # Тут непонятно как к автору обращаться
                    author=row[3],
                    score=row[4],
                    pub_date=row[5]
                )
                review.save()

    def handle(self, *args, **options):
        self.genre_load()
        self.category_load()
        self.comments_load()
        self.genre_title_load()
        self.review_load()
        self.users_load()
