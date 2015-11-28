#conding: utf-8
from django.db import models


class Cash(models.Model):

	date = models.DateField('Dia', null=False, blank=False)
	history = models.CharField('Histórico', max_length=100, null=False, blank=False)
	income = models.DecimalField('Entrada', max_digits=20, decimal_places=2, default=0.0)
	expenses = models.DecimalField('Saida', max_digits=20, decimal_places=2, default=0.0)

	@property
	def total(self):
		'''
			Total from the instanced object.
		'''
		return self.income - self.expenses

	@staticmethod
	def total_value():
		'''
			Total from all objects.
		'''
		incomes = sum(item.income for item in Cash.objects.all())
		expenses = sum(item.expenses for item in Cash.objects.all())
		return incomes - expenses

	@staticmethod
	def list_years():
		'''
			Return a list of years that there are objects cash saved.
		'''
		cashs = Cash.objects.all()
		years = [c.date.year for c in cashs]

		dicio = {}
		for year in years:
			dicio[year] = 1

		return list(dicio.keys())

	@staticmethod
	def filter_by_date(day=None, month=None, year=None):
		filters = {
			'date__day':day, 
			'date__month':month, 
			'date__year':year,
		}
		filters.update(filters)

		filter_by = {
			key:value for key, value in filters.items() if value is not None
		}

		return Cash.objects.filter(**filter_by)

	@staticmethod
	def total_value_by_date(day=None, month=None, year=None):
		filters = {
			'date__day':day, 
			'date__month':month, 
			'date__year':year,
		}
		filters.update(filters)

		filter_by = {
			key:value for key, value in filters.items() if value is not None
		}

		incomes = sum(
				item.income for item in Cash.objects.filter(
					**filter_by
				)
			)
		expenses = sum(
				item.expenses for item in Cash.objects.filter(
					**filter_by
				)
			)
		return incomes - expenses

	class Meta:
		ordering = ['date']
		verbose_name = ('Cash')
		verbose_name_plural = ('Cash')