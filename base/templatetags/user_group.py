from django import template
import calendar
from base.models import RateRent, Rents
register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='get_month_name')
def get_month_name(value):
    return calendar.month_name[value]

@register.filter(name='get_rating')
def get_rating(value):
    rent = Rents.objects.filter(vehicle__id=value)
    ratings = RateRent.objects.filter(rent__in=rent)
    if ratings.count() > 0:
        average = 0
        for rating in ratings:
            average += rating.rating
        return str(average / ratings.count())
    else:
        return "N/A"



register.filter('get_rating', get_rating)
register.filter('has_group', has_group)
register.filter('get_month_name', get_month_name)

