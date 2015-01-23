from django.db import models
from django.utils.datetime_safe import datetime
from estofadora.client.models import Client

class Item(models.Model):

	client = models.ForeignKey(Client, blank=False, null=False, related_name='client')

	name = models.CharField('Nome', max_length=256, blank=False, null=False)
	description = models.TextField('', blank=False, null=False)
	concluded = models.BooleanField('Concluido', default=False)
	arrived_date = models.DateTimeField('Chegou', auto_now_add=True)	
	delivery_date = models.DateTimeField('Entrega')
	total_value = models.DecimalField('Valor total', max_digits=20, decimal_places=2, default=0.0)
	total_paid = models.DecimalField('Valor pago', max_digits=20, decimal_places=2, default=0.0)

	class Meta:
		verbose_name = 'Item'
		verbose_name_plural = 'Itens'

	def rest_value(self):
		return (float(self.total_value) - float(self.total_paid))

	def __str__(self):
		return self.name

	def __unicode__():
		return self.name