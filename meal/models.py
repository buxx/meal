from datetime import datetime

from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from paypal.standard.ipn.models import PayPalIPN

RESERVATION_STATE_WAITING_PAYMENT = 'WAITING_PAYMENT'
RESERVATION_STATE_RESERVED = 'RESERVED'
RESERVATION_STATE_CANCELLED_BY_USER = 'CANCELLED_BY_USER'
RESERVATION_STATE_CANCELLED_BY_ADMIN = 'CANCELLED_BY_ADMIN'
RESERVATION_STATE_CANCELLED_BY_UNPAYMENT = 'CANCELLED_BY_UNPAYMENT'
RESERVATION_STATES = (
    (RESERVATION_STATE_WAITING_PAYMENT, _('Attente de paiement')),
    (RESERVATION_STATE_RESERVED, _('Réservé')),
    (RESERVATION_STATE_CANCELLED_BY_USER, _('Annulé (Client)')),
    (RESERVATION_STATE_CANCELLED_BY_ADMIN, _('Annulé (Admin)')),
    (RESERVATION_STATE_CANCELLED_BY_UNPAYMENT, _('Annulé (Pas de paiement)')),
)

TRANSACTION_STATUS_NEW = 'NEW'
TRANSACTION_STATUS_PENDING = 'PENDING'
TRANSACTION_STATUS_ERROR = 'ERROR'
TRANSACTION_STATUS_COMPLETED = 'COMPLETED'
TRANSACTION_STATUSES = (
    (TRANSACTION_STATUS_NEW, _('Nouvelle')),
    (TRANSACTION_STATUS_ERROR, _('Erreur')),
    (TRANSACTION_STATUS_PENDING, _('En attente')),
    (TRANSACTION_STATUS_COMPLETED, _('Complété')),
)


class User(AbstractUser):
    group = models.ForeignKey(
        'Group',
        verbose_name=_('Groupe'),
        related_name='members',
        blank=True,
        null=True,
    )


class Group(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Nom'),
        error_messages={
            'unique': _('Ce nom est déjà utilisée.'),
        },
    )
    creator = models.ForeignKey(
        User,
        related_name='created_groups',
        blank=False,
        null=False,
    )

    def __str__(self):
        return self.name

    @property
    def members_str(self):
        members_str = ', '.join([user.get_full_name() for user in self.members.all()])
        if not members_str:
            return ', '.join([user.email for user in self.members.all()])
        return members_str


class Day(models.Model):
    date = models.DateField(
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('Jour réservable'),
        error_messages={
            'unique': _('Ce jour existe déjà'),
        }
    )
    cancelled = models.BooleanField(
        null=False,
        default=False,
    )
    price = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_('Prix en CENTIMES'),
    )

    class Meta:
        ordering = ('date',)

    @property
    def active(self):
        return not self.cancelled

    def __str__(self):
        return str(self.date)


class Reservation(models.Model):
    state = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=RESERVATION_STATES,
    )
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='reservations',
        verbose_name=_('Utilisateur'),
    )
    day = models.ForeignKey(
        Day,
        null=False,
        blank=False,
        related_name='reservations',
        verbose_name=_('Jour'),
    )
    price = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_('Prix en CENTIMES'),
    )

    class Meta:
        ordering = ('day__date',)
        # TODO: On doit pouvoir réserver un our annulé (par client)
        unique_together = ('user', 'day',)

    def __str__(self):
        return '{0} {1}'.format(
            self.day.date,
            self.user,
        )

    @property
    def state_str(self):
        return dict(RESERVATION_STATES)[self.state]


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='transactions',
        verbose_name=_('Utilisateur'),
    )
    reservations = models.ManyToManyField(
        Reservation,
        related_name='transactions',
        verbose_name=_('Réservations'),
    )
    status = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        choices=TRANSACTION_STATUSES,
        default=TRANSACTION_STATUS_NEW,
    )
    paypal_status = models.CharField(
        max_length=255,
        null=False,
        blank=True,
        default='',
    )
    price = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_('Prix en CENTIMES'),
    )
    logs = models.TextField(
        null=False,
        blank=True,
        default='',
    )
    ipns = models.ManyToManyField(
        PayPalIPN,
        related_name='transactions',
        verbose_name=_('IPNs'),
    )


class ContactMessage(models.Model):
    created = models.DateTimeField(
        default=datetime.now,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='messages',
        verbose_name=_('Utilisateur'),
    )
    message = models.TextField(
        null=False,
        blank=False,
    )

    class Meta:
        ordering = ['-created']
