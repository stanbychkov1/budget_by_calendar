from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserAdminCustom(UserAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_superuser',
    )
    list_filter = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')


admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
