from django.contrib.admin import ModelAdmin, register

from titles.models import Category, Genre, Title
from reviews.models import Comment, Review


@register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_editable = ('score',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date'
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@register(Genre)
class GenreAdmin(ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@register(Title)
class TitleAdmin(ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('description', 'category', 'genre')
    empty_value_display = '-пусто-'
