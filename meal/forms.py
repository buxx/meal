from datetime import datetime, timedelta

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from paypal.standard.forms import PayPalPaymentsForm

from meal.models import User
from meal.models import Menu
from meal.models import Day
from meal.models import Group
from meal_booking.forms import ModelForm
from meal_booking.forms import RequiredFieldsMixin
from meal_booking.utils import WEEK_DAYS
from meal_booking.utils import get_complete_day_id_list


class CurrentUserForm(RequiredFieldsMixin, ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'group',
        )
        fields_required = (
            'first_name',
            'last_name',
        )


class CreateGroupForm(RequiredFieldsMixin, ModelForm):
    class Meta:
        model = Group
        fields = (
            'name',
        )
        fields_required = (
            'name',
        )


class DaysRangeForm(forms.Form):
    start_day = forms.DateField(
        required=True,
        widget=AdminDateWidget,
    )
    end_day = forms.DateField(
        required=True,
        widget=AdminDateWidget,
    )
    days = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=WEEK_DAYS,
    )

    def clean(self):
        if 'start_day' in self.cleaned_data and 'end_day' in self.cleaned_data:
            if self.cleaned_data['start_day'] > self.cleaned_data['end_day']:
                raise ValidationError(
                    _('Dates invalides: la date de début doit précéder la date de fin'),
                )

        if 'days' in self.cleaned_data and 'start_day' in self.cleaned_data:
            if str(self.cleaned_data['start_day'].weekday()) not in self.cleaned_data['days']:
                raise ValidationError(
                    _('Le jour de départ doit être un des jours de la semaine choisis'),
                )

        if 'days' in self.cleaned_data and 'end_day' in self.cleaned_data:
            if str(self.cleaned_data['end_day'].weekday()) not in self.cleaned_data['days']:
                raise ValidationError(
                    _('Le jour de fin doit être un des jours de la semaine choisis'),
                )

        return super().clean()


class CreateDaysForm(DaysRangeForm):
    price = forms.IntegerField(
        required=True,
        label=_('Prix en CENTIMES'),
    )

    def clean(self):
        if 'start_day' in self.cleaned_data and 'end_day' in self.cleaned_data:
            if self.cleaned_data['start_day'] > self.cleaned_data['end_day']:
                raise ValidationError(
                    _('Dates invalides: la date de début doit précéder la date de fin'),
                )

        if 'days' in self.cleaned_data and 'start_day' in self.cleaned_data:
            if str(self.cleaned_data['start_day'].weekday()) not in self.cleaned_data['days']:
                raise ValidationError(
                    _('Le jour de départ doit être un des jours de la semaine choisis'),
                )

        if 'days' in self.cleaned_data and 'end_day' in self.cleaned_data:
            if str(self.cleaned_data['end_day'].weekday()) not in self.cleaned_data['days']:
                raise ValidationError(
                    _('Le jour de fin doit être un des jours de la semaine choisis'),
                )

        return super().clean()


class ChooseDaysForm(forms.Form):
    days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.none(),  # Will be replaced in __init__
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        current_week_strftime = datetime.utcnow().strftime("%Y-W%W-1")
        current_week_datetime = datetime.strptime(current_week_strftime, "%Y-W%W-%w")
        three_weeks_datetime = current_week_datetime + timedelta(days=20)

        self.fields['days'].queryset = Day.objects\
            .filter(
                cancelled=False,
                date__gte=current_week_datetime,
                date__lte=three_weeks_datetime,
            )

    def clean(self):
        days = self.cleaned_data['days']
        complete_day_id_list = get_complete_day_id_list()
        complete_errors = []

        if days:
            for day in days:
                if day.id in complete_day_id_list:
                    complete_errors.append(ValidationError(
                        'Le jour {0} est déjà complet'.format(day.date)
                    ))

        if complete_errors:
            raise ValidationError(complete_errors)


class PaymentForm(PayPalPaymentsForm):
    pass


class ContactForm(forms.Form):
    message = forms.CharField(
        required=True,
        widget=forms.Textarea
    )


class MenuForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Menu
        fields = ('start_day', 'message')
