# conding: utf-8
from django import forms
from .models import Bill


class BillForm(forms.ModelForm):

    class Meta:
        model = Bill
        fields = ['name', 'date_to_pay', 'value']

    def __init__(self, *args, **kwargs):
        super(BillForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_to_pay'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['value'].widget.attrs.update(
            {'class': 'form-control'}
        )

    def clean(self):
        cleaned_data = super(BillForm, self).clean()
        name = cleaned_data.get('name')
        date_to_pay = cleaned_data.get('date_to_pay')

        if Bill.objects.filter(name=name, date_to_pay=date_to_pay).exists():
            raise forms.ValidationError(
                'Já existe uma conta com esse nome e data.'
            )
        return self.cleaned_data
