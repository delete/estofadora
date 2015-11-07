import os

from django.db import models
from django.utils.datetime_safe import datetime
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

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


def image_path(data, filename):
    "Returns the filepath where the image is store"
    extension = data.image.path[data.image.path.find('.'):]
    return os.path.join('items/images/{0}/{0}{1}'.format(data.item.name, extension))


class Picture(models.Model):

	item = models.ForeignKey(Item, blank=False, null=False, related_name='pictures')
	created_at = models.DateField('Criado em', auto_now_add=True)
	image = models.ImageField(
		upload_to=image_path, verbose_name="Imagem",
		null=False, blank=False
	)

	class Meta:
		verbose_name = 'Imagem'
		verbose_name_plural = 'Imagens'

	def __str__(self):
		return '{0} - {1}'.format(self.item.name, self.created_at.isoformat())


# Delete the file associated with the model instance
@receiver(post_delete, sender=Picture)
def mymodel_delete(sender, instance, **kwargs):
	if instance.image:
		instance.image.delete(False)
