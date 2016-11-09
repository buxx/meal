from django import forms
from django.contrib import admin

from meal.forms import MenuForm
from meal.models import Group
from meal.models import Menu
from meal.models import ContactMessage
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
    list_filter = ('date', 'cancelled', 'price')


class ReservationAdmin(admin.ModelAdmin):
    #  TODO: utiliser un champ date dans le day
    fields = ('day', 'user', 'state', 'price')
    list_display = ('day', 'user', 'state', 'transactions_resume', 'price')
    list_filter = (
        'day__date',
        'user__first_name',
        'user__last_name',
        'state',
        'price',
        'user__group',
        'transactions__status',
    )


class TransactionAdmin(admin.ModelAdmin):
    fields = ('user', 'status', 'paypal_status', 'price', 'reservations', 'ipns', 'logs')
    list_display = ('user', 'status', 'price')
    list_filter = ('user__first_name', 'user__last_name', 'status', 'price')


class ContactMessageAdmin(admin.ModelAdmin):
    fields = ('created', 'user', 'message')
    list_display = ('created', 'user')
    search_fields = (
        'user',
        'message',
    )
    list_filter = ('created', 'user__first_name', 'user__last_name')


class MenuAdmin(admin.ModelAdmin):
    form = MenuForm
    fields = ('start_day', 'message')
    list_display = ('start_day',)
    search_fields = (
        'message',
    )
    list_filter = ('start_day',)

admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Menu, MenuAdmin)
