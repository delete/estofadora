import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from estofadora.core.utils import MONTHS

from .forms import CashForm
from .models import Cash


@login_required
def home(request):
	return render(request, 'statement/statement.html')


@login_required
def cash(request):
	context = {}
	date = datetime.datetime.now().date()
	
	content = Cash.objects.filter(date=date)
	total_value = Cash.total_value_by_date(date=date)

	form = CashForm()

	if request.method == 'POST':
		
		if 'search_form' in request.POST:
			date = request.POST.get('search_date')
			try:
				date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
			except ValueError:
				date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
			
			content = Cash.objects.filter(date=date)
			total_value = Cash.total_value_by_date(date=date)

		else:
		
			form = CashForm(request.POST)

			if form.is_valid():
				form.save()
				messages.success(request, 'Registrado com sucesso!')
				form = CashForm()
				return redirect(reverse('statement:cash'))

	context['form'] = form
	context['content'] = content
	context['total_value'] = total_value
	context['choose_date'] = date
	return render(request, 'statement/cash.html', context)


@login_required
def delete(request, pk):
	cash = get_object_or_404(Cash, pk=pk)
	cash.delete()
	messages.success(request, 'Registro removido com sucesso!')
	return redirect(reverse('statement:cash'))


@login_required
def edit(request, pk):
	context = {}
	cash = get_object_or_404(Cash, pk=pk)

	if request.method == 'POST':
		form = CashForm(request.POST, instance=cash)
		if form.is_valid():
			form.save()
			return render(request, 'statement/item_edit_form_success.html', {'item': cash})
		else:
			context['form_error'] = True
	else:
		form = CashForm(instance=cash)

	context['form'] = form
	context['item'] = cash
	return render(request, 'statement/item_edit_form.html', context)


@login_required
def cash_month(request):
	context = {}
	date = datetime.datetime.now().date()

	content = Cash.filter_by_month_year(date)
	total_value = Cash.total_value_by_month_year(date)

	if request.method == 'POST':
		month = request.POST.get('selectmonth')
		year = request.POST.get('selectyear')
		
		#Create a datetime object
		date = datetime.datetime(int(year), int(month), 1).date()

		content = Cash.filter_by_month_year(date)
		total_value = Cash.total_value_by_month_year(date)

	context['content'] = content
	context['total_value'] = total_value
	context['choose_date'] = date
	context['months'] = MONTHS
	context['years'] = Cash.list_years()
	return render(request, 'statement/cash_month.html', context)