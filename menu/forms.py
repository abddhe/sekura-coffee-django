from django import forms
from .models import Order, Item, Comment
from datetime import datetime, timedelta


class OrderForm(forms.ModelForm):
    receive_time = forms.CharField(required=False)

    class Meta:
        model = Order
        fields = ['receive_time', "order_accept"]

    def clean_receive_time(self):
        try:
            if not hasattr(self, 'receive_time'):
                self.receive_time = 15
            time = int(self.receive_time)
            new_receive = (datetime.now() + timedelta(minutes=time)).time()
            return new_receive
        except ValueError:
            raise forms.ValidationError('The receive time must as number')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('order', 'body')
