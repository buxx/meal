from meal.models import User
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
