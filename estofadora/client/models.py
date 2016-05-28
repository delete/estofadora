# conding: utf-8
from django.db import models


class Client(models.Model):

    name = models.CharField('Nome', max_length=200)
    email = models.EmailField('Email', unique=True, blank=True)
    adress = models.CharField(
        u'Endereço', max_length=256
    )
    telephone1 = models.CharField('Telefone 1', max_length=15)
    telephone2 = models.CharField('Telefone 2', max_length=15, blank=True)
    is_active = models.BooleanField(u'Está ativo?', default=True)
    date_join = models.DateTimeField('Data de cadastro', auto_now_add=True)

    class Meta:
        ordering = ['date_join']
        verbose_name = ('cliente')
        verbose_name_plural = ('clientes')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
