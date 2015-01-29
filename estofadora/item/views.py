from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
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


@login_required
def list(request):
	context = {}

	if request.method == 'POST':
		client_name = request.POST.get('name')
		items = Item.objects.filter(client__name__icontains=client_name)
		if not items:
			messages.warning(request, 'Nenhum item cadastrado para esse cliente!')
	else:
		items = Item.objects.all()
		if not items:
			messages.warning(request, 'Nenhum item cadastrado!')

	context['items'] = items
	return render(request, 'item/list.html', context)


@login_required
def delete(request, pk):
	item = get_object_or_404(Item, pk=pk)
	item.delete()
	messages.success(request, 'Item removido com sucesso!')
	return redirect(reverse('item:list'))