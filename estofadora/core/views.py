from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from estofadora.item.models import Item, Picture


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