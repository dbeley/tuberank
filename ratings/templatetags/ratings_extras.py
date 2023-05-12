from urllib.parse import urlencode

from django import template
from django.utils.translation import gettext as _

register = template.Library()


@register.filter
def duration(seconds: int):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60
    if hours > 0:
        return _("%(hours)sH %(minutes)sm %(seconds)ss") % {
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }
    return _("%(minutes)sm %(seconds)ss") % {"minutes": minutes, "seconds": seconds}


@register.filter
def custom_rating(value: int | float) -> float:
    return round(value / 2, 2)


@register.simple_tag
def urlparams(*_, **kwargs):
    safe_args = {k: v for k, v in kwargs.items() if v is not None}
    if safe_args:
        return "?{}".format(urlencode(safe_args))
    return ""
