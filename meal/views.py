from django.shortcuts import redirect
from django.urls import reverse
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


def index_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return redirect(reverse('account_login'))


class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {}
