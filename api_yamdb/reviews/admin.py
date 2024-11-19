from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from reviews.constants import ADDITIONAL_USER_FIELDS
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


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
class CategoryAdmin(TagMixin, admin.ModelAdmin):
    pass


class GenreTabular(admin.TabularInline):
    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
        'get_genres'
    )
    list_editable = (
        'year',
        'description',
        'category'
    )
    inlines = (GenreTabular,)
    search_fields = ('name',)
    list_filter = ('genre', 'category',)
    list_display_links = ('name',)

    @admin.display(description='genres')
    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])


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
class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = ADDITIONAL_USER_FIELDS + BaseUserAdmin.fieldsets
    add_fieldsets = ADDITIONAL_USER_FIELDS + BaseUserAdmin.add_fieldsets
