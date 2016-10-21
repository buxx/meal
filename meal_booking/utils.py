from django.conf import settings
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
