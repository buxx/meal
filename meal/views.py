from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic

from meal.forms import CurrentUserForm
from meal.models import User


@method_decorator(login_required, name='dispatch')
class EditCurrentUserView(generic.UpdateView):
    model = User
    template_name = 'update_current_user.html'
    form_class = CurrentUserForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        messages.add_message(
            self.request,
            level=messages.SUCCESS,
            message=_('Les modifications ont été prisent en compte')
        )
        return super().get_success_url()


def index_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    return redirect(reverse('account_login'))


@method_decorator(login_required, name='dispatch')
class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'user': self.request.user,
        }
