from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from estofadora.item.models import Item


@login_required
def home(request):
	return render(request, 'index.html')

def site(request):
	return render(request, 'site/site_index.html')

def portfolio(request):
	context = {}
	items = Item.objects.all()

	context['items'] = items
	return render(request, 'site/portfolio.html', context)