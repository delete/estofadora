from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views .generic import CreateView
from django.utils.decorators import method_decorator
from django.forms.formsets import formset_factory, BaseFormSet

from .forms import ItemForm, ItemPictureForm, PictureForm
from .models import Item, Picture


@login_required
def add(request):
	context = {}
	
	if request.method == 'POST':
		item_picture_form = ItemPictureForm(request.POST, request.FILES)

		if item_picture_form.is_valid():
			item_picture_form.save()
			
			messages.success(request, 'Item cadastrado com sucesso!')
			item_picture_form = ItemPictureForm()

	else:
		item_picture_form = ItemPictureForm()

	context['item_picture_form'] = item_picture_form
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
			return redirect(
					reverse('client:list_items', args=[item.client.pk])
				)
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

	else:
		items = Item.objects.all()

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

	if request.method == 'POST':

		# Adding a new image
		if 'add-form' in request.POST:
			picture_form = PictureForm(request.POST, request.FILES)

			if picture_form.is_valid():
				picture_form.save(instance=item, commit=False)
				messages.success(request, 'Imagem enviada com sucesso!')
				return redirect(reverse('item:image_list', args=[item.pk]))

		# Changing image' states
		else:
			checked_ids = request.POST.getlist('checks[]')
			selected_states = request.POST.getlist('selects[]')

			# Create a list because will be need to remove itens
			all_pictures = [p for p in pictures]
			
			all_pictures = removeCheckedPictureFromAllPictures(checked_ids, all_pictures)

			setFalseInRemainPictures(all_pictures)

			setTrueInCheckedPictures(checked_ids)

			if selected_states:
				for selected in selected_states:
					_id, state = tuple(selected.split('_'))
					
					picture = get_object_or_404(Picture, pk=_id)
					picture.state = state
					picture.save()
				
			messages.success(request, 'Alterado com sucesso!')
			return redirect(reverse('item:image_list', args=[item.pk]))

	context['item'] = item
	context['pictures'] = pictures
	context['picture_form'] = PictureForm()
	return render(request, 'item/list_images.html', context)


def removeCheckedPictureFromAllPictures(checked_ids, all_pictures):
	for picture in all_pictures:
		for check in checked_ids:
			if int(picture.pk) == int(check):
				all_pictures.remove(picture)
	return all_pictures

def setFalseInRemainPictures(all_pictures):
	for picture in all_pictures:
		picture.public = False
		picture.save()

def setTrueInCheckedPictures(checked_ids):
	for check in checked_ids:
		picture = get_object_or_404(Picture, pk=check)
		picture.public = True
		picture.save()


@login_required
def image_delete(request, pk):
	picture = get_object_or_404(Picture, pk=pk)
	item = picture.item
	picture.delete()
	messages.success(request, 'Imagem removida com sucesso!')
	
	return redirect(reverse('item:image_list', args=[item.pk]))