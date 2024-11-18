from django.contrib import admin
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User
)


class TagMixin:
    list_display = (
        'name',
        'slug'
    )
    list_editable = (
        'name',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('slug',)


@admin.register(Genre)
class GenreAdmin(TagMixin, admin.ModelAdmin):
    pass


@admin.register(Category)
class GenreAdmin(TagMixin, admin.ModelAdmin):
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category'
    )
    list_editable = (
        'year',
        'description',
        'category'
    )
    search_fields = ('name',)
    list_filter = ('genre', 'category',)
    list_display_links = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'pub_date',
        'score',
        'title'
    )
    list_editable = ('text',)
    list_filter = ('score', 'pub_date', 'score')
    list_display_links = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'review',
        'pub_date'
    )

    list_editable = ('text',)
    search_fields = ('text', 'author',)
    list_filter = ('pub_date', 'author', 'review')
    list_display_links = ('author',)


@admin.register(User)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio',
        'is_staff',
        'is_active',
        'date_joined'
    )
    list_editable = (
        'email',
        'bio',
        'role',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio',
        'is_staff',
        'is_active',
        'date_joined'
    )
    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )
    list_display_links = ('username',)
