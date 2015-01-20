#coding: utf-8
from django.utils.datetime_safe import datetime
from django.contrib import admin
from estofadora.client.models import Client

class ClientAdmin(admin.ModelAdmin):
	list_display = ('name', 'adress', 'email', 'telephone1', 'is_active')
	search_fields = ('name', 'adress', 'email', 'telephone1', 'telephone2')
	date_hierarchy = 'date_join'
	list_filter = ['date_join']

	def subscribed_today(self, obj):
		return obj.date_join.date() == datetime.today().date()

	subscribed_today.short_description = (u'Cadsatrado hoje?')
	subscribed_today.boolean = True

	def mark_as_active(self, request, queryset):
		count = queryset.update(is_active=True)

		msg = u'%d clientes ativos.'

		self.message_user(request, msg % count)

	mark_as_active.short_description = ('Marcar como ativo')

admin.site.register(Client, ClientAdmin)