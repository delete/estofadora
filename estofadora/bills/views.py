from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from .forms import BillForm
from .models import Bill


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


@login_required
def list(request):
	context = {}
	bills = Bill.objects.all()

	context['bills'] = bills
	return render(request, 'bills/list.html', context)


@login_required
def delete(request, pk):
	bill = get_object_or_404(Bill, pk=pk)

	bill.delete()

	messages.success(request, 'Conta removida com sucesso!')
	return redirect(reverse('bills:list'))
