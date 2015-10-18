import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from .forms import CashForm
from .models import Cash


@login_required
def home(request):
	return render(request, 'statement/statement.html')


@login_required
def cash(request):
	context = {}
	now = datetime.datetime.now().date()
	
	content = Cash.objects.filter(date=now)
	total_value = Cash.total_value_by_date(date=now)

	form = CashForm()

	if request.method == 'POST':
		
		if 'search_form' in request.POST:
			date = request.POST.get('search_date')
			date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
			
			content = Cash.objects.filter(date=date)
			total_value = Cash.total_value_by_date(date=date)
			context['choose_date'] = date

		else:
		
			form = CashForm(request.POST)

			if form.is_valid():
				form.save()
				messages.success(request, 'Registrado com sucesso!')
				form = CashForm()

	context['form'] = form
	context['content'] = content
	context['total_value'] = total_value
	return render(request, 'statement/cash.html', context)


@login_required
def delete(request, pk):
	cash = get_object_or_404(Cash, pk=pk)
	cash.delete()
	messages.success(request, 'Registro removido com sucesso!')
	return redirect(reverse('statement:cash'))