from meal.models import User
from meal_booking.forms import ModelForm


class CurrentUserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'group',
        )
