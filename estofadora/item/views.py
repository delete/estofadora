from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views .generic import CreateView
from django.utils.decorators import method_decorator
from django.forms.formsets import formset_factory, BaseFormSet

from .forms import ItemForm, PictureFormSet
from .models import Item, Picture


@login_required
def add(request):
	context = {}
	
	if request.method == 'POST':
		item_form = ItemForm(request.POST)
		picture_formset = PictureFormSet(request.POST, request.FILES)

		if item_form.is_valid() and picture_formset.is_valid():
			object = item_form.save()
			picture_formset.instance = object
			picture_formset.save()
			messages.success(request, 'Item cadastrado com sucesso!')

	else:
		item_form = ItemForm()
		picture_formset = PictureFormSet()

	context['item_form'] = item_form
	context['picture_formset'] = picture_formset
	return render(request, 'item/add.html', context)


@login_required
def edit(request, pk):
	context = {}
	item = get_object_or_404(Item, pk=pk)

	if request.method == 'POST':
		form = ItemForm(request.POST, instance=item)

		if form.is_valid():
			form.save()
			messages.success(request, 'Item alterado com sucesso!')
	else:	
		form = ItemForm(instance=item)

	context['form'] =  form
	context['item'] = item
	return render(request, 'item/edit.html', context)


@login_required
def list(request):
	context = {}

	if request.method == 'POST':
		client_name = request.POST.get('name')
		items = Item.objects.filter(client__name__icontains=client_name)

		if not items:
			messages.warning(request, 'Nenhum item cadastrado para esse cliente!')

	else:
		items = Item.objects.all()

		if not items:
			messages.warning(request, 'Nenhum item cadastrado!')

	context['items'] = items
	return render(request, 'item/list.html', context)


@login_required
def delete(request, pk):
	item = get_object_or_404(Item, pk=pk)
	item.delete()
	messages.success(request, 'Item removido com sucesso!')
	
	return redirect(reverse('item:list'))


@login_required
def image_list(request, pk):
	context = {}
	item = get_object_or_404(Item, pk=pk)

	pictures = Picture.objects.filter(item=item)

	if not pictures:
			messages.warning(request, 'Nenhuma imagem adicionada!')

	context['item'] = item
	context['pictures'] = pictures
	return render(request, 'item/list_images.html', context)


@login_required
def image_delete(request, pk):
	picture = get_object_or_404(Picture, pk=pk)
	item = picture.item
	picture.delete()
	messages.success(request, 'Imagem removida com sucesso!')
	
	return redirect(reverse('item:image_list', args=[item.pk]))