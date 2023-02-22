from django import forms
from .models import Order,Item

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_num', 'items']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].widget = forms.CheckboxSelectMultiple()
        self.fields['items'].queryset = Item.objects.filter(available=True)
