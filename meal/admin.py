from django.contrib import admin

from meal.models import Group, User


class GroupAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )


class UserAdmin(admin.ModelAdmin):
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
