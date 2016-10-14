from django import forms
from django.contrib import admin

from meal.models import Group, User
from meal_booking.forms import ModelForm


class GroupAdminForm(ModelForm):
    related = ['members']
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Group
        fields = ('name', 'creator')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'members_str')
    search_fields = (
        'name',
    )
    form = GroupAdminForm


class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'last_name', 'first_name', 'group')
    list_display = ('email', 'last_name', 'first_name', 'group')
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
