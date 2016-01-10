from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from estofadora.core.utils import MONTHS, last_day_of, month_before_of

from .forms import CashForm
from .models import Cash, Balance


@login_required
def home(request):
    return render(request, 'statement/statement.html')


@login_required
def cash(request):
    context = {}
    date = datetime.now().date()

    content = Cash.objects.filter(date=date)

    form = CashForm(initial={'date': date})

    if request.method == 'POST':

        if 'search_form' in request.POST:
            date = request.POST.get('search_date')
            try:
                date = datetime.strptime(date, '%d/%m/%Y').date()
            except ValueError:
                date = datetime.strptime(date, '%Y-%m-%d').date()

            content = Cash.objects.filter(date=date)

        else:

            form = CashForm(request.POST)

            if form.is_valid():
                form.save()

                messages.success(request, 'Registrado com sucesso!')

                return redirect(reverse('statement:cash'))

    total_before = Balance.total_balance_before(date)
    content, balance = Cash.create_balance(content, total_before)

    context['form'] = form
    context['content'] = content
    context['total_value'] = balance
    context['total_before'] = total_before
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
            return render(
                request, 'statement/item_edit_form_success.html',
                {'item': cash}
            )
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
    date = datetime.now().date()
    year = date.year
    month = date.month

    content = Cash.filter_by_date(month=month, year=year)
    total_value = Cash.total_value_by_date(month=month, year=year)

    if request.method == 'POST':
        month = int(request.POST.get('selectmonth'))
        year = int(request.POST.get('selectyear'))

        content = Cash.filter_by_date(month=month, year=year)
        total_value = Cash.total_value_by_date(month=month, year=year)

    y, m = month_before_of(year, month)
    last_day_month_before = last_day_of(y, m)

    total_before = Balance.total_balance_before(last_day_month_before)

    content, total_value = Cash.create_balance(content, total_before)

    context['content'] = content
    context['total_value'] = total_value
    context['total_before'] = total_before
    context['choose_month'] = month
    context['choose_year'] = year
    context['months'] = MONTHS
    context['years'] = Cash.list_years()
    return render(request, 'statement/cash_month.html', context)


@login_required
def cash_annual(request):
    context = {}
    year = datetime.now().date().year

    content = Cash.filter_by_date(year=year)
    total_value = Cash.total_value_by_date(year=year)

    if request.method == 'POST':
        year = int(request.POST.get('selectyear'))

        content = Cash.filter_by_date(year=int(year))
        total_value = Cash.total_value_by_date(year=year)

    january = 1
    y, m = month_before_of(year, january)
    last_day_year_before = last_day_of(y, m)

    total_before = Balance.total_balance_before(last_day_year_before)

    content, total_value = Cash.create_balance(content, total_before)

    context['total_value'] = total_value
    context['total_before'] = total_before
    context['content'] = content
    context['choose_year'] = year
    context['years'] = Cash.list_years()

    return render(request, 'statement/cash_annual.html', context)
