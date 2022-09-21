"""Админка приложения 'reviews'."""
from django.contrib import admin

from .models import Categories, Comments, Genres, GenreTitle, Review, Title


class CategoriesAdmin(admin.ModelAdmin):
    """Админка категорий."""
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    """Админка жанров."""
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    """Админка произведений."""
    list_display = ('id', 'name', 'year', 'description', 'category',)
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    """Админка произведений и жанров."""
    list_display = ('id', 'title_id', 'genre_id',)
    list_editable = ('title_id', 'genre_id',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Админка ревью."""
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date',)
    list_editable = ('title', 'author',)
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    """Админка комментариев."""
    list_display = ('id', 'review_id', 'text', 'author', 'pub_date',)
    list_editable = ('review_id', 'author',)
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
