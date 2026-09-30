from django import template
from django.utils import timezone
register = template.Library()

@register.filter
def hue(name): return sum(map(ord, name)) * 53 % 360

@register.filter
def initial(user):
    name = user.get_full_name() or user.username
    return "".join(w[0] for w in name.split()[:2]).upper()

@register.filter
def ago(dt):
    s = int((timezone.now() - dt).total_seconds())
    if s < 60: return "now"
    if s < 3600: return f"{s // 60}m"
    if s < 86400: return f"{s // 3600}h"
    if s < 7 * 86400: return f"{s // 86400}d"
    return dt.strftime("%b %d")
