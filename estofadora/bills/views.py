from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from .forms import BillForm


@login_required
def new(request):
	context = {}

	if request.method == 'POST':
		
		form = BillForm(request.POST)

		if form.is_valid():
			form.save()
			messages.success(request, 'Cadastrada com sucesso!')
			return redirect(reverse('bills:new'))
	else:
		form = BillForm()

	context['form'] = form
	return render(request, 'bills/new.html', context)
