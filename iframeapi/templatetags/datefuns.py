from dateutil.relativedelta import relativedelta
from datetime import date
from django import template

register = template.Library()


@register.filter(name='age')
def age(birthday):
    return relativedelta(date.today(), birthday).years
