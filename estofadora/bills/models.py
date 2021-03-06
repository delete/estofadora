# conding: utf-8
from django.db import models

from estofadora.statement.models import Cash


class Bill(models.Model):
    '''
        Class that model bills to pay. Like: water, internet, telephone, ...
    '''

    date_to_pay = models.DateField('Dia')
    name = models.CharField('Nome', max_length=200)
    value = models.DecimalField(
        'Valor', max_digits=20, decimal_places=2, default=0.0
    )
    is_paid = models.BooleanField(u'Está paga?', default=False)

    class Meta:
        ordering = ['date_to_pay']
        verbose_name = ('Conta')
        verbose_name_plural = ('Contas')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''
            When a BIll is created, a Cash object is created
            too.
        '''
        data = {
            'date': self.date_to_pay,
            'history': self.name,
            'income': 0,
            'expenses': self.value,
        }
        Cash.objects.create(**data)

        # Call the "real" save() method.
        super(Bill, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''
            When a Bill is deleted, a related Cash object must be
            deleted too.
        '''
        cash = Cash.objects.get(date=self.date_to_pay, history=self.name)
        cash.delete()

        # Call the "real" delete() method.
        super(Bill, self).delete(*args, **kwargs)
