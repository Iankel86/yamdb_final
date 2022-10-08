from django.contrib.admin import ModelAdmin, register

from users.models import CustomUser

ModelAdmin.empty_value_display = '-пусто-'


@register(CustomUser)
class UserAdmin(ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'role', 'bio',
        'first_name', 'last_name', 'confirmation_code')
    list_editable = ('role',)
    search_fields = ('username', 'email')
