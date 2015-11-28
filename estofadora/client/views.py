#conding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from estofadora.item.models import Item

from .forms import ClientForm
from .models import Client


@login_required
def add(request):
	context = {}

	if request.method == 'POST':

		form = ClientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Cliente cadastrado com sucesso!')
			return redirect('client:list')
	else:
		form = ClientForm()

	context['form'] = form
	return render(request, 'client/add.html', context)


@login_required
def edit(request, pk):
	context = {}
	client = get_object_or_404(Client, pk=pk)

	if request.method == 'POST':
		form = ClientForm(request.POST, instance=client)
		if form.is_valid():
			form.save()
			messages.success(request, 'Cliente alterado com sucesso!')
			return redirect(reverse('client:list'))
	else:
		form = ClientForm(instance=client)

	context['form'] = form
	context['client'] = client
	return render(request, 'client/edit.html', context)


@login_required
def list(request):
	context = {}

	if request.method == 'POST':
		client_name = request.POST.get('name')
		clients = Client.objects.filter(
					name__icontains=client_name
				).order_by('name')

	else:
		clients = Client.objects.all().order_by('name')


	context['clients'] = clients
	return render(request, 'client/list.html', context)


@login_required
def delete(request, pk):
	client = get_object_or_404(Client, pk=pk)
	client.delete()
	messages.success(request, 'Cliente removido com sucesso!')
	return redirect(reverse('client:list'))


@login_required
def list_items(request, pk):
	context = {}

	client = get_object_or_404(Client, pk=pk)
	items = Item.objects.filter(client=client)

	context['items'] = items
	context['client'] = client
	context['amount'] = len(items)
	context['total'] = sum(item.total_value for item in items)
	context['received'] = sum(item.total_paid for item in items)
	context['owing'] = True if context['received']<context['total'] else False
	return render(request, 'client/list_items.html', context)