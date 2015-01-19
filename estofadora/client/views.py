from django.shortcuts import render
from django.contrib import messages

from estofadora.client.forms import ClientForm


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
