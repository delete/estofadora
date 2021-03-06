from django.db import models


class Contact(models.Model):

    name = models.CharField('Nome', max_length=200)
    email = models.CharField('Email', max_length=200, null=True, blank=True)
    telephone = models.CharField(
        'Telefone', max_length=15, null=True, blank=True
    )
    subject = models.CharField(
        'Assunto', max_length=30
    )
    description = models.TextField('Mensagem')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    read = models.BooleanField('Lido', default=False)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.email)
