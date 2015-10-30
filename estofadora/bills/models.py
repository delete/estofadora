#conding: utf-8
from django.db import models

from estofadora.statement.models import Cash


class Bill(models.Model):

	date_to_pay = models.DateField('Dia', null=False, blank=False)
	name = models.CharField('Nome', max_length=200, null=False, blank=False)
	value = models.DecimalField('Valor', max_digits=20, decimal_places=2, default=0.0)
	is_paid = models.BooleanField(u'Está paga?', default=False)

	def save(self, *args, **kwargs):
		data = {
			'date': self.date_to_pay,
			'history': self.name,
			'income': 0,
			'expenses': self.value,
		}
		Cash.objects.create(**data)

		# Call the "real" save() method.
		super(Bill, self).save(*args, **kwargs) 

	class Meta:
		ordering = ['date_to_pay']
		verbose_name = ('Conta')
		verbose_name_plural = ('Contas')

	def __str__(self):
		return self.name

	def __unicode__():
		return self.name
