#conding: utf-8
from django.db import models


class Cash(models.Model):

	date = models.DateField('Dia', null=False, blank=False)
	history = models.CharField('Histórico', max_length=100, null=False, blank=False)
	income = models.DecimalField('Entrada', max_digits=20, decimal_places=2, default=0.0)
	expenses = models.DecimalField('Saida', max_digits=20, decimal_places=2, default=0.0)

	@property
	def total(self):
		return self.income - self.expenses

	@staticmethod
	def total_value():
		incomes = sum(item.income for item in Cash.objects.all())
		expenses = sum(item.expenses for item in Cash.objects.all())
		return incomes - expenses

	@staticmethod
	def total_value_by_date(date):
		incomes = sum(item.income for item in Cash.objects.filter(date=date))
		expenses = sum(item.expenses for item in Cash.objects.filter(date=date))
		return incomes - expenses

	@staticmethod
	def total_value_by_month_year(date):
		incomes = sum(item.income for item in Cash.objects.filter(date__month=date.month, date__year=date.year))
		expenses = sum(item.expenses for item in Cash.objects.filter(date__month=date.month, date__year=date.year))
		return incomes - expenses

	@staticmethod
	def filter_by_month_year(date):
		return Cash.objects.filter(
			date__month=date.month, date__year=date.year
		)

	@staticmethod
	def list_years():
		'Get a list of years that there object cash saved.'
		cashs = Cash.objects.all()
		years = [c.date.year for c in cashs]

		dicio = {}
		for year in years:
			dicio[year] = 1

		return list(dicio.keys())

	class Meta:
		ordering = ['date']
		verbose_name = ('Cash')
		verbose_name_plural = ('Cash')