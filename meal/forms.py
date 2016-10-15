from meal.models import User
from meal.models import Group
from meal_booking.forms import ModelForm
from meal_booking.forms import RequiredFieldsMixin


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
