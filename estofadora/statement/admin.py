#coding: utf-8
from django.utils.datetime_safe import datetime
from django.contrib import admin
from estofadora.statement.models import Cash

class CashAdmin(admin.ModelAdmin):
	list_display = ('date', 'history', 'income', 'expenses', 'total')
	search_fields = ('date', 'history')
	date_hierarchy = 'date'
	list_filter = ['date']

	def subscribed_today(self, obj):
		return obj.date.date() == datetime.today().date()

	subscribed_today.short_description = (u'Cadastrado hoje?')
	subscribed_today.boolean = True


admin.site.register(Cash, CashAdmin)
