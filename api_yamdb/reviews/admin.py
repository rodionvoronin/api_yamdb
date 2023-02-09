from django.contrib import admin

from .models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

"""
#@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
"""

class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role',
                  'bio', 'first_name', 'last_name')


# вывод данных на странице
class ImportAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]


#admin.site.register(User, UserAdmin)
admin.site.register(User, ImportAdmin)
