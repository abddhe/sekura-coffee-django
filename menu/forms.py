from django import forms
from .models import Order, Item


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["items", "table", 'receive_time', "total_price", "order_accept"]

