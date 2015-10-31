#coding: utf-8
from django.utils.datetime_safe import datetime
from django.contrib import admin

from estofadora.bills.models import Bill


class BillAdmin(admin.ModelAdmin):
	list_display = ('name', 'date_to_pay', 'value', 'is_paid')
	search_fields = ('name', 'date_to_pay')
	date_hierarchy = 'date_to_pay'
	list_filter = ['date_to_pay']

	def need_to_pay_today(self, obj):
		return obj.date_to_pay.date() == datetime.today().date()

	need_to_pay_today.short_description = (u'Pagar hoje?')
	need_to_pay_today.boolean = True

	def mark_as_paid(self, request, queryset):
		count = queryset.update(is_paid=True)

		msg = u'%d contas pagas.'

		self.message_user(request, msg % count)

	mark_as_paid.short_description = ('Marcar como pago')

admin.site.register(Bill, BillAdmin)