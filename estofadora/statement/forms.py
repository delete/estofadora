# conding: utf-8
from django import forms
from .models import Cash


class CashForm(forms.ModelForm):

    class Meta:
        model = Cash
        fields = ['date', 'history', 'income', 'expenses']

    def __init__(self, *args, **kwargs):
        super(CashForm, self).__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'form-control'})
        self.fields['history'].widget.attrs.update({'class': 'form-control'})
        self.fields['income'].widget.attrs.update({'class': 'form-control'})
        self.fields['expenses'].widget.attrs.update({'class': 'form-control'})
