#conding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from estofadora.client.forms import ClientForm
from estofadora.client.models import Client


@login_required
def add(request):
	context = {}

	if request.method == 'POST':

		form = ClientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Cliente cadastrado com sucesso!')
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
	else:
		form = ClientForm(instance=client)

	context['form'] = form
	context['client'] = client
	return render(request, 'client/edit.html', context)


@login_required
def list(request):
	context = {}

	context['clients'] = Client.objects.order_by('name')
	return render(request, 'client/list.html', context)


@login_required
def delete(request, pk):
	client = get_object_or_404(Client, pk=pk)
	client.delete()
	messages.success(request, 'Cliente removido com sucesso!')
	return redirect(reverse('client:list'))