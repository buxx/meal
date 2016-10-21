from django import forms
from django.contrib import admin

from meal.models import Group
from meal.models import Transaction
from meal.models import Reservation
from meal.models import User
from meal.models import Day
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


class DayAdmin(admin.ModelAdmin):
    fields = ('date', 'cancelled', 'price')
    list_display = ('date', 'active', 'price')
    search_fields = (
        'date',
    )


class ReservationAdmin(admin.ModelAdmin):
    fields = ('day', 'user', 'state', 'price')
    list_display = ('day', 'user', 'state', 'price')
    #  TODO: utiliser un champ date dans le day


class TransactionAdmin(admin.ModelAdmin):
    fields = ('user', 'status', 'paypal_status', 'price', 'reservations', 'ipns', 'logs')
    list_display = ('user', 'status', 'price')

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Transaction, TransactionAdmin)
