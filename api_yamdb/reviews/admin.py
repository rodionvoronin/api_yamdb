from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Category, Comment, Genre, Review, Title, User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role',
                  'bio', 'first_name', 'last_name')


class ImportUserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ImportCategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class ImportGenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ImportTitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'year', 'description')
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        exclude = ('title_id',)
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title_id')
        skip_unchanged = True
        report_skipped = True
        raise_errors = False


class ImportReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]
    list_display = ('id', 'text', 'score', 'author', 'pub_date', 'title')
    search_fields = ('id', 'text', 'score', 'author', 'pub_date', 'title')
    list_filter = ('author', 'pub_date')
    empty_value_display = '-пусто-'


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
        fields = ('id', 'review_id', 'text', 'author', 'pub_date')


class ImportCommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]
    list_display = ('id', 'author', 'review', 'text', 'pub_date')
    search_fields = ('id', 'author', 'review', 'text', 'pub_date')
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(User, ImportUserAdmin)
admin.site.register(Category, ImportCategoryAdmin)
admin.site.register(Genre, ImportGenreAdmin)
admin.site.register(Title, ImportTitleAdmin)
admin.site.register(Review, ImportReviewAdmin)
admin.site.register(Comment, ImportCommentAdmin)
