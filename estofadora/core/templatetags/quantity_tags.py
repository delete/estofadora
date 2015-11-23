from django import template

from estofadora.client.models import Client
from estofadora.item.models import Item, Picture
from estofadora.bills.models import Bill


register = template.Library()


@register.simple_tag
def get_clients():
    return Client.objects.filter(is_active=True).count()


@register.simple_tag
def get_items():
    return Item.objects.count()

@register.simple_tag
def get_pictures():
    return Picture.objects.count()

@register.simple_tag
def get_bills():
    return Bill.objects.count()