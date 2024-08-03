from django.contrib import admin
from typing import Any

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('pub_date',)

    @admin.display(description='Средний рейтинг')
    def get_average_score(self, obj):
        return obj.get_average_score()


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ('pub_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'slug')


@admin.register(Title)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'get_genres',
                    'get_average_score')
    search_fields = ('name', 'category__name')
    empty_value_display = '-пусто-'
    list_editable = ('name', 'category')
    list_filter = ('category', 'genre__name')
    inlines = (GenreTitleInline, ReviewInline)

    def get_genres(self, obj: Any) -> str:
        return ', '.join([genre.name for genre in obj.genre.all()])

    get_genres.short_description = 'Жанры'  # type: ignore

    def get_average_score(self, obj: Any) -> float:
        return obj.get_average_score()

    get_average_score.short_description = 'Средний рейтинг'  # type: ignore


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    empty_value_display = '-пусто-'
    list_editable = ('text', 'author', 'score')
    list_filter = ('author', 'title')
    inlines = (CommentInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review', 'author', 'text', 'pub_date')
    search_fields = ('text', 'author__username', 'review__text')
    empty_value_display = '-пусто-'
    list_filter = ('author', 'review')
