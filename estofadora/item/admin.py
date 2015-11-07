#coding: utf-8
from django.utils.datetime_safe import datetime
from django.contrib import admin
from estofadora.item.models import Item, Picture

class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'arrived_date', 'delivery_date', 'total_paid', 'total_value')
	search_fields = ('name', 'description')
	date_hierarchy = 'arrived_date'
	list_filter = ['arrived_date']

	def subscribed_today(self, obj):
		return obj.arrived_date.date() == datetime.today().date()

	subscribed_today.short_description = (u'Cadastrado hoje?')
	subscribed_today.boolean = True

	def mark_as_concluded(self, request, queryset):
		count = queryset.update(concluded=True)

		msg = u'%d itens concluidos.'

		self.message_user(request, msg % count)

	mark_as_concluded.short_description = ('Marcar como concluido')


class PictureAdmin(admin.ModelAdmin):
	list_display = ('item', 'created_at',)
	search_fields = ('item',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Picture, PictureAdmin)
