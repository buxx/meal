from django.conf import settings
from django.db.models import Count
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


DAY_LUN = 0
DAY_MAR = 1
DAY_MER = 2
DAY_JEU = 3
DAY_VEN = 4
DAY_SAM = 5
DAY_DIM = 6

WEEK_DAYS = (
    (DAY_LUN, _('Lundi')),
    (DAY_MAR, _('Mardi')),
    (DAY_MER, _('Mercredi')),
    (DAY_JEU, _('Jeudi')),
    (DAY_VEN, _('Vendredi')),
    (DAY_SAM, _('Samedi')),
    (DAY_DIM, _('Dimanche')),
)


def get_paypal_ipn_url():
    return '{0}{1}'.format(
        settings.PAYPAL_BASE_URL,
        reverse('paypal-ipn'),
    )


def get_complete_day_id_list() -> [int]:
    from meal.models import Reservation
    return Reservation.objects \
        .values('day_id') \
        .annotate(cnt=Count('id')) \
        .filter(cnt__gte=settings.MAXIMUM_RESERVATION_PER_DAY) \
        .values_list('day_id', flat=True)
