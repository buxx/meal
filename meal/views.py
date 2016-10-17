from copy import copy
from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from allauth.account.views import LoginView as BaseLoginView

from meal.forms import CurrentUserForm
from meal.forms import DaysRangeForm
from meal.forms import CreateDaysForm
from meal.forms import CreateGroupForm
from meal.models import User
from meal.models import Day
from meal.models import Group


class LoginView(BaseLoginView):
    success_url = reverse_lazy('home')


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


@method_decorator(login_required, name='dispatch')
class CreateGroupView(generic.CreateView):
    template_name = 'create_group.html'
    form_class = CreateGroupForm
    model = Group

    def get_success_url(self):
        messages.add_message(
            self.request,
            level=messages.SUCCESS,
            message=_('Groupe créé et assigné avec succès'),
        )
        return reverse_lazy('home')

    def form_valid(self, form):
        group = form.save(commit=False)
        group.creator = self.request.user
        group.save()

        group.members = [self.request.user]
        group.save()

        self.object = group

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(permission_required('admin'), name='dispatch')
class CreateDays(generic.FormView):
    template_name = 'admin/meal/day/create_days.html'
    form_class = CreateDaysForm
    success_url = '/admin/meal/day/'  # TODO: ? reverse_lazy('admin.days')

    def get_initial(self) -> dict:
        return {
            'price': '8,50',  # TODO: In admin config
            'days': settings.AVAILABLE_DAYS,  # TODO: In admin config
        }

    def form_valid(self, form):
        end_day = form.cleaned_data['end_day']
        start_day = form.cleaned_data['start_day']
        time_delta = end_day - start_day
        one_day = timedelta(days=1)
        days = []

        current_date = copy(start_day)
        for i in range(time_delta.days+1):
            if str(current_date.weekday()) not in form.cleaned_data['days']:
                # This day is not in selected days
                current_date += one_day
                continue

            days.append(Day(
                date=current_date,
                price=form.cleaned_data['price'],
            ))
            current_date += one_day

        already_exists_days = []
        created_days = []

        # TODO savemultiple at once ?
        for day in days:
            try:
                day.save()
                created_days.append(day)
            except IntegrityError:
                already_exists_days.append(day)

        if not already_exists_days:
            messages.add_message(
                self.request,
                level=messages.SUCCESS,
                message=_('{0} jour(s) ont été créé(s)'
                          .format(len(created_days))),
            )
        elif created_days:
            messages.add_message(
                self.request,
                level=messages.WARNING,
                message=_(
                    '{0} existaient déjà mais '
                    '{1} jour(s) ont été créé(s)'
                    .format(
                        len(already_exists_days),
                        len(created_days),
                    )),
            )
        else:
            messages.add_message(
                self.request,
                level=messages.ERROR,
                message=_('Aucun jour n\'a été créé: Il ou ils '
                          'existaient déjà')
            )

        return redirect(self.get_success_url())


class ReservationsView(generic.FormView):
    form_class = DaysRangeForm
    template_name = 'reservations.html'
