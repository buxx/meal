from copy import copy
from datetime import timedelta, datetime

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
from django.views.decorators.csrf import csrf_exempt

from meal.forms import CurrentUserForm
from meal.forms import ContactForm
from meal.forms import PaymentForm
from meal.forms import ChooseDaysForm
from meal.forms import CreateDaysForm
from meal.forms import CreateGroupForm
from meal.models import User
from meal.models import Menu
from meal.models import Transaction
from meal.models import ContactMessage
from meal.models import Reservation
from meal.models import RESERVATION_STATE_WAITING_PAYMENT
from meal.models import Day
from meal.models import Group
from meal.templatetags.meal_extras import format_price
from meal_booking.utils import get_paypal_ipn_url
from meal import pay  # Needed to connect signals


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


@method_decorator(login_required, 'dispatch')
class ReservationsView(generic.FormView):
    form_class = ChooseDaysForm
    template_name = 'reservations.html'

    def get_context_data(self, **kwargs):
        kwargs['reservations'] = self.request.user.reservations.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # TODO: Validator in form: user must have group
        # TODO: Template: message if not in group
        reservations = []
        for day in form.cleaned_data['days']:
            reservations.append(
                Reservation(
                    day=day,
                    user=self.request.user,
                    price=day.price,
                    state=RESERVATION_STATE_WAITING_PAYMENT,
                )
            )

        for reservation in reservations:
            reservation.save()

        return redirect(reverse('pay'))

    def post(self, request, *args, **kwargs):
        if not self.request.user.group:
            messages.add_message(
                self.request,
                level=messages.ERROR,
                message=_('Vous devez appartenir à un groupe pour '
                          'pouvoir effectuer une réservation'),
            )
            form = self.get_form()
            return self.form_invalid(form)
        return super().post(request, *args, **kwargs)


@login_required
@csrf_exempt
def return_to_reservations(request):
    messages.add_message(
        request,
        level=messages.SUCCESS,
        message=_('La demande de paiement à été reçue. '
                  'Vos réservations vont être validées.'),
    )
    return redirect(reverse('reservations'))


@login_required
@csrf_exempt
def cancel_to_reservations(request):
    messages.add_message(
        request,
        level=messages.WARNING,
        message=_('Le paiement n\' pas été enregistré'),
    )
    return redirect(reverse('reservations'))


@method_decorator(login_required, 'dispatch')
class PreparePaymentView(generic.TemplateView):
    template_name = 'prepare_payment.html'

    def get_context_data(self, **kwargs):
        reservations = Reservation.objects.filter(
            user=self.request.user,
            state=RESERVATION_STATE_WAITING_PAYMENT,
        ).all()

        if not reservations:
            return redirect(reverse('reservations'))

        amount_in_cents = sum([r.price for r in reservations])

        # Create related transaction
        transaction = Transaction(
            user=self.request.user,
            price=amount_in_cents,
            logs='{0}: {1}'.format(
                str(datetime.utcnow()),
                'CREATE',
            )
        )
        transaction.save()

        transaction.reservations = reservations
        transaction.save()

        # TODO: Creer qqpart un numero d'invoice qui liste les jours,
        # sinon on peux ayer pour des reservation faites entre temps
        form = PaymentForm(initial={
            "business": settings.PAYPAL_BUSINESS_ID,
            "amount": format_price(amount_in_cents),
            "item_name": "Réservation de {0} jour(s)".format(len(reservations)),
            "invoice": transaction.pk,
            "notify_url": get_paypal_ipn_url(),
            "return_url": self.request.build_absolute_uri(reverse('return_to_reservations')),
            "cancel_return": self.request.build_absolute_uri(reverse('cancel_to_reservations')),
            "currency_code": "EUR",
        })

        kwargs.update({
            'form': form,
            'reservations': reservations,
            'amount': amount_in_cents,
        })
        return super().get_context_data(**kwargs)


@method_decorator(login_required, 'dispatch')
class ContactView(generic.FormView):
    template_name = 'contact.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        kwargs['phone_number'] = settings.PHONE_NUMBER
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        message = ContactMessage(
            user=self.request.user,
            message=form.cleaned_data['message'],
        )
        message.save()
        messages.add_message(
            self.request,
            level=messages.SUCCESS,
            message=_('Le message à bien été enregistré et envoyé'),
        )
        return redirect(reverse('reservations'))


@method_decorator(login_required, 'dispatch')
class MenuListView(generic.ListView):
    model = Menu
    template_name = 'menu_list.html'


@method_decorator(login_required, 'dispatch')
class MenuDetailView(generic.DetailView):
    model = Menu
    template_name = 'menu_detail.html'
