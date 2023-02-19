from django.contrib import admin
from reviews.models import YaMdbUser


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )
    search_fields = ('username',)


admin.site.register(YaMdbUser)
