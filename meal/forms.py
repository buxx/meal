from meal.models import User
from meal_booking.forms import ModelForm
from meal_booking.forms import RequiredFieldsMixin


class CurrentUserForm(RequiredFieldsMixin, ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'group',
        )
        fields_required = (
            'email',
            'first_name',
            'last_name',
        )
