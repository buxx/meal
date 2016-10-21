from datetime import datetime

from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.models import ST_PP_PENDING
from paypal.standard.ipn.signals import valid_ipn_received

from meal.models import Transaction
from meal.models import RESERVATION_STATE_RESERVED
from meal.models import TRANSACTION_STATUS_ERROR
from meal.models import TRANSACTION_STATUS_PENDING
from meal.models import TRANSACTION_STATUS_COMPLETED


def valid_ipn_received_watcher(sender, **kwargs):
    ipn_obj = sender

    transaction = Transaction.objects.get(pk=ipn_obj.invoice)
    transaction.paypal_status = ipn_obj.payment_status

    ipn_amount = ipn_obj.mc_gross * 100
    if transaction.price != ipn_amount:
        transaction.status = TRANSACTION_STATUS_ERROR
        transaction.logs = '{0}\n{1}: {2}'.format(
            transaction.logs,
            datetime.utcnow(),
            'INCORRECT AMOUNT ({0} vs {1})'.format(
                transaction.price,
                ipn_amount,
            ),
        )
        transaction.save()
        return

    if settings.PAYPAL_BUSINESS_ID != ipn_obj.receiver_email:
        transaction.status = TRANSACTION_STATUS_ERROR
        transaction.logs = '{0}\n{1}: {2}'.format(
            transaction.logs,
            datetime.utcnow(),
            'INCORRECT PAYPAL_BUSINESS_ID ({0} vs {1})'.format(
                settings.PAYPAL_BUSINESS_ID,
                ipn_obj.receiver_email,
            ),
        )
        transaction.save()
        return

    mark_reserved = False
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        mark_reserved = True
        transaction.status = TRANSACTION_STATUS_COMPLETED
        transaction.logs = '{0}\n{1}: COMPLETED'.format(
            transaction.logs,
            datetime.utcnow(),
        )
    elif ipn_obj.payment_status == ST_PP_PENDING:
        mark_reserved = True
        transaction.status = TRANSACTION_STATUS_PENDING
        transaction.logs = '{0}\n{1}: PENDING'.format(
            transaction.logs,
            datetime.utcnow(),
        )
    else:
        transaction.status = TRANSACTION_STATUS_ERROR
        transaction.logs = '{0}\n{1}: {2}'.format(
            transaction.logs,
            datetime.utcnow(),
            'INVALID STATUS ({0})'.format(
                ipn_obj.payment_status,
            ),
        )

    transaction.save()
    if mark_reserved:
        for reservation in transaction.reservations.all():
            reservation.state = RESERVATION_STATE_RESERVED
            reservation.save()


valid_ipn_received.connect(valid_ipn_received_watcher)
