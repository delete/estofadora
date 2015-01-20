from django.db import models


class Client(models.Model):

	name = models.CharField('Nome', max_length=200, null=False, blank=False)
	email = models.EmailField('Email', unique=True, blank=True)
	adress = models.CharField(u'Endereço', max_length=256, null=False, blank=False)
	telephone1 = models.CharField('Telefone 1', max_length=15, blank=False)
	telephone2 = models.CharField('Telefone 2', max_length=15, blank=True)
	is_active = models.BooleanField(u'Está ativo?', default=True)
	date_join = models.DateTimeField('Data de cadastro', auto_now_add=True)

	class Meta:
		ordering = ['date_join']
		verbose_name = ('cliente')
		verbose_name_plural = ('clientes')