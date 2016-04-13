# coding: utf-8
from django import forms

from multiupload.fields import MultiFileField

from estofadora.client.models import Client

from .models import Item, Picture


class ItemForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=Client.objects.all(), label="Cliente")
    description = forms.CharField(label="Descrição", widget=forms.Textarea)

    class Meta:
        model = Item
        fields = [
            'client', 'name', 'delivery_date',
            'total_value', 'total_paid', 'description', 'concluded'
        ]

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['delivery_date'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['total_value'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['total_paid'].widget.attrs.update(
            {'class': 'form-control'}
        )


class ItemPictureForm(ItemForm):

    files = MultiFileField(
            label="Imagens", min_num=0, max_num=10, max_file_size=1024*1024*5,
            required=False
        )

    def save(self, commit=True):
        instance = super(ItemPictureForm, self).save(commit)

        for each in self.cleaned_data['files']:
            Picture.objects.create(image=each, item=instance)

        return instance


class PictureForm(forms.Form):

    files = MultiFileField(
            label="Imagens", min_num=0, max_num=10, max_file_size=1024*1024*5
        )

    def save(self, instance, commit=True):

        for each in self.cleaned_data['files']:
            Picture.objects.create(image=each, item=instance)
