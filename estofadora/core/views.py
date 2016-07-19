import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from estofadora.item.models import Item, Picture
from estofadora.bills.models import Bill

from .forms import ContactForm
from .models import Contact


@login_required
def home(request):
    context = {}

    # Every week has a number, get the atual number.
    this_week = datetime.datetime.now().isocalendar()[1]

    # Get all items and separate them which the week number matchs
    items = Item.objects.all().order_by('-delivery_date')

    items_to_delivery = [
        i for i in items if i.delivery_date.isocalendar()[1] == this_week
    ]

    # Gell all bills and separate them which the week number matchs
    bills = Bill.objects.all().order_by('-date_to_pay')

    week_bills = [
        b for b in bills if b.date_to_pay.isocalendar()[1] == this_week
    ]

    context['items'] = items_to_delivery
    context['bills'] = week_bills
    context['section'] = 'home'
    return render(request, 'index.html', context)


def site(request):
    context = {}

    pictures = Picture.objects.filter(
        public=True, state='after').order_by('-created_at')[:4]
    context['pictures'] = pictures
    return render(request, 'site/site_index.html', context)


def portfolio(request):
    context = {}
    items = Item.objects.all()

    context['items'] = items
    return render(request, 'site/portfolio.html', context)


def contact(request):
    context = {}

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, 'Obrigado pela mensagem, entraremos em contato!'
            )
            return redirect(reverse('core:contact'))
    else:
        form = ContactForm()

    context['form'] = form
    return render(request, 'site/contact.html', context)


@login_required
def contactMessages(request):
    context = {}

    contactMessages = Contact.objects.all().order_by('-created_at')

    context['contactMessages'] = contactMessages
    context['section'] = 'messages'
    return render(request, 'contactMessages.html', context)


@login_required
def deleteMessage(request, pk):
    contact = get_object_or_404(Contact, pk=pk)

    contact.delete()

    messages.success(request, 'Mensagem removida com sucesso!')
    return redirect(reverse('core:contactMessages'))


@login_required
def markMessageAsRead(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.read = True
    contact.save()

    messages.success(request, 'Mensagem lida!')
    return redirect(reverse('core:contactMessages'))
