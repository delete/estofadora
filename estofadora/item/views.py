from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ItemForm
from .models import Item


@login_required
def add(request):
	context = {}
	
	if request.method == 'POST':
		form = ItemForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'Item cadastrado com sucesso!')
	else:
		form = ItemForm()

	context['form'] = form
	return render(request, 'item/add.html', context)



@login_required
def edit(request, pk):
	context = {}
	item = get_object_or_404(Item, pk=pk)

	if request.method == 'POST':
		form = ItemForm(request.POST, instance=item)

		if form.is_valid():
			form.save()
			messages.success(request, 'Item alterado com sucesso!')
	else:	
		form = ItemForm(instance=item)

	context['form'] =  form
	return render(request, 'item/edit.html', context)