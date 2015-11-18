from django import template
from estofadora.core.models import Contact

register = template.Library()


@register.simple_tag
def get_mensagens():
    return Contact.objects.all().count()