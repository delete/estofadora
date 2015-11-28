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
	total_value = Cash.total_value_by_date(
					day=date.day, month=date.month, year=date.year
				)

	form = CashForm()

	if request.method == 'POST':
		
		if 'search_form' in request.POST:
			date = request.POST.get('search_date')
			try:
				date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
			except ValueError:
				date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
			
			content = Cash.objects.filter(date=date)
			total_value = Cash.total_value_by_date(
							day=date.day, month=date.month, year=date.year
						)

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
	year = date.year
	month = date.month

	content = Cash.filter_by_date(month=month, year=year)
	total_value = Cash.total_value_by_date(month=month, year=year)

	if request.method == 'POST':
		month = int(request.POST.get('selectmonth'))
		year = int(request.POST.get('selectyear'))
		
		content = Cash.filter_by_date(month=month, year=year)
		total_value = Cash.total_value_by_date(month=month, year=year)

	context['content'] = content
	context['total_value'] = total_value
	context['choose_month'] = month
	context['choose_year'] = year
	context['months'] = MONTHS
	context['years'] = Cash.list_years()
	return render(request, 'statement/cash_month.html', context)


@login_required
def cash_annual(request):
	context = {}
	year = datetime.datetime.now().date().year

	content = Cash.filter_by_date(year=year)
	total_value = Cash.total_value_by_date(year)

	if request.method == 'POST':
		year = int(request.POST.get('selectyear'))

		content = Cash.filter_by_date(year=int(year))
		total_value = Cash.total_value_by_date(year=year)


	context['total_value'] = total_value
	context['content'] = content
	context['choose_year'] = year
	context['years'] = Cash.list_years()

	return render(request, 'statement/cash_annual.html', context)