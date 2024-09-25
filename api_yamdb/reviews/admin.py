from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
        'role',
    )
    list_editable = (
        'first_name',
        'last_name',
        'role',
        'email',
        'bio'
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    def get_genre_list(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])

    get_genre_list.short_description = 'Жанры'

    search_fields = ('name',)
    list_display = (
        'name',
        'year',
        'description',
        'category',
        'get_genre_list',
    )
    list_editable = ('year', 'category')
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
