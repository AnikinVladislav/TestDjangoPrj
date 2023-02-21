from django import forms
from .models import *

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = "datetime-local"
 
class DateTimeLocalField(forms.DateTimeField):

    input_formats = [
        "%Y-%m-%dT%H:%M:%S", 
        "%Y-%m-%dT%H:%M:%S.%f", 
        "%Y-%m-%dT%H:%M"
    ]
    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")



class SpendingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=categories.objects.all(), empty_label='category not selected',widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = spendings
        fields = ('date', 'category', 'amount', 'user')

        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount:',
                'step': '0.01'
            }),
            'date': DateTimeLocalInput(attrs={
                'class': 'form-control'
            }),
            'user': forms.HiddenInput(attrs={
                'class': 'form-select'
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if float(amount) < 0:
            raise forms.ValidationError('Amount must be positive')
        print(self.cleaned_data)
        return amount

class CategoryForm(forms.ModelForm):
    class Meta:
        model = categories
        fields = ('description',)

        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category:'
            }),
        }

