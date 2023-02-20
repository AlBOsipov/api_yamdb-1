from django.contrib import admin
from reviews.models import YaMdbUser, Title, Genre, Category, GenreTitle


admin.site.register(YaMdbUser)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(GenreTitle)
