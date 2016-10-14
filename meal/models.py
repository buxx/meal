from django.contrib.auth.models import UserManager
from django.utils.translation import ugettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models


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
