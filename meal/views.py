from django.urls import reverse_lazy
from django.views import generic

from meal.forms import CurrentUserForm
from meal.models import User


class EditCurrentUserView(generic.UpdateView):
    model = User
    template_name = 'update_current_user.html'
    form_class = CurrentUserForm
    success_url = reverse_lazy('edit_current_user')

    def get_object(self, queryset=None):
        return self.request.user
