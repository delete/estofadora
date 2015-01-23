from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ItemForm


@login_required
def add(request):
	context = {}
	
	if request.method == 'POST':
		
		form = ItemForm(request.POST)
		if form.is_valid():
			form.save()
	else:
		form = ItemForm()

	messages.success(request, 'Item cadastrado com sucesso!')
	context['form'] = form
	return render(request, 'item/add.html', context)
