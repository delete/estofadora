#conding: utf-8
from django.db import models
from django.db import IntegrityError, transaction


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

	@staticmethod
	def create_balance(content, total_before):
		"""
			Create a new temporary field (balance) that will save the amount of
			balance before plus the atual item total. Example:

			ITEM  TOTAL  BALANCE
			item0 -1000  -1000    (item0.total + total from the day before)
			item1 +500   -500     (item1.total + item0.balance)
			item2 +600   100      (item2.total + item1.balance)
			etc...
			"""
		last_element = len(content) - 1
		balance = 0

		for index, item in enumerate(content):
			if index == 0:
				item.balance = item.total + total_before
			else:
				item.balance = content[index-1].balance + (item.total)

			# The last one has the total
			if index == last_element:
				balance = item.balance
		
		return content, balance

	
	def save(self, *args, **kwargs):
		# Need instance balance obj to store the total value
		try:
			#If exists will raise IntegrityError.
			with transaction.atomic():
				obj = Balance(date=self.date, value=self.total)
				obj.save()

		except IntegrityError:
			# Get the balance and update
			obj = Balance.objects.get(date=self.date)
			obj.value += self.total
			obj.save()

		# Call the "real" save() method.
		super(Cash, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		obj = Balance.objects.get(date=self.date)
		obj.value -= self.total

		if obj.value == float(0):
			obj.delete()
		else:
			obj.save()

		super(Cash, self).delete(*args, **kwargs)


	class Meta:
		ordering = ['date']
		verbose_name = ('Cash')
		verbose_name_plural = ('Cash')


class Balance(models.Model):

	date = models.DateField('Dia', unique=True)
	value = models.DecimalField('Valor', max_digits=20, decimal_places=2, default=0.0)

	@staticmethod
	def total_balance_before(date):
		items = Balance.objects.filter(date__lt=date)

		total = sum(i.value for i in items)

		return total

	class Meta:
		ordering = ['date']
		verbose_name = ('Balance')
		verbose_name_plural = ('Balance')