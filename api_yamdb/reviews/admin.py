from django.contrib import admin

from users.models import User
from .models import Category, Comment, Genre, Review, Title


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'bio',
        'role',
    )
    list_editable = (
        'role',
        'email'
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = (
        'name',
        'year',
        'description',
        'category'
    )
    list_editable = (
        'year',
    )
    list_filter = ('category',)
    filter_horizontal = ('genre',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    list_editable = (
        'slug',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    list_editable = (
        'slug',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'title',
        'score',
        'pub_date'
    )
    list_filter = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'review',
        'pub_date'
    )
