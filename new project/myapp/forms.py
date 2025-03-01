from django import forms
from myapp.models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name'
        }
        widgets = {
            'client': forms.RadioSelect()
        }

class InterestForm(forms.Form):
    INTEREST_CHOICES = [
        (1, 'Yes'),
        (0, 'No'),
    ]
    interested = forms.ChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.RadioSelect,
        label='Are you interested?'
    )
    quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        label='Quantity'
    )
    comments = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Additional Comments'
    )
