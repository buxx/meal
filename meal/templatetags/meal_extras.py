from datetime import datetime

from django import template

from meal.models import User
from meal.models import Reservation
from meal.models import RESERVATION_STATE_RESERVED
from meal.models import RESERVATION_STATE_WAITING_PAYMENT

register = template.Library()


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)


def to_date(value):
    """Convert to date date in 2016-10-16 format"""
    return datetime.strptime(value, '%Y-%m-%d')


def week_number(datetime):
    return datetime.isocalendar()[1]


def reserved_or_trying(day_date: datetime, user: User) -> bool:
    return bool(
        Reservation.objects.filter(
            user=user,
            day__date=day_date,
            state__in=(
                RESERVATION_STATE_WAITING_PAYMENT,
                RESERVATION_STATE_RESERVED,
            )
        )
        .count()
    )


def format_price(price_in_cents: int):
    return '{price:02}'.format(price=price_in_cents/100)


def contains_waiting_payments(reservations: ['Reservation']) -> bool:
    for reservation in reservations:
        if reservation.state == RESERVATION_STATE_WAITING_PAYMENT:
            return True
    return False

register.filter('to_date', to_date)
register.filter('week_number', week_number)
register.tag('assign', do_assign)
register.filter('reserved_or_trying', reserved_or_trying)
register.filter('format_price', format_price)
register.filter('contains_waiting_payments', contains_waiting_payments)
