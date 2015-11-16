from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from estofadora.item.models import Item, Picture

from .forms import ContactForm


@login_required
def home(request):
	return render(request, 'index.html')

def site(request):
	context = {}

	pictures = Picture.objects.filter(state='after').order_by('-created_at')[:4]
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
			messages.success(request, 'Obrigado pela mensagem, entraremos em contato!')
			return redirect(reverse('core:contact'))
	else:
		form = ContactForm()
	
	context['form'] = form
	return render(request, 'site/contact.html', context)