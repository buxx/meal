from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from meal.models import User
from meal.models import Day
from meal.models import Group
from meal_booking.forms import ModelForm
from meal_booking.forms import RequiredFieldsMixin
from meal_booking.utils import WEEK_DAYS


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
        # TODO: la query set doit exclure les cancelled et ceux ou il
        # y a count(reservations) > où réservation sont valides
        # TODO: Il faut aussi se debrouiller pour avoir que 2
        # semaine dans le futur
        queryset=Day.objects.filter(
            cancelled=False,
        ),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )
    # TODO: Car il ne faut pas réserver un jour ou il y a trop de monde, jour cancel, etc
