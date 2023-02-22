from django.shortcuts import get_object_or_404, redirect, render,get_list_or_404
from django.views.generic import (CreateView, UpdateView , TemplateView, ListView, DetailView)

from menu.forms import OrderForm
from .models import (Category, Item,Order)
from datetime import datetime
from django.urls import reverse_lazy


# Create your views here.
class HomeView(TemplateView):
    template_name = 'menu/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AboutUsView(HomeView):
    template_name = 'menu/about-us.html'


class ContactUsView(HomeView):
    template_name = 'menu/contact-us.html'


class OrderListView(HomeView):
    template_name = 'menu/orders.html'

"""
class AddToOrderview(CreateView):
    model=Order
    fields=['table_num']
    template_name="menu/add_to_order.html"
    
    def form_valid(self, form) :
         # Get the item to add to the order
        item = get_object_or_404(Item, pk=self.kwargs['pk'])

        # Get the table number from the form
        table_num = form.cleaned_data['table_num']

        # Get or create the order
        order, created = Order.objects.get_or_create(
            table_num=table_num,
            order_accept=False,
            receive_time=None,
            defaults={'total_price': 0.0}
        )

        # Add the item to the order
        order.items.add(item)

        # Calculate the new total price for the order
        order.total_price += item.price
        order.save()

        return redirect('order_detail', pk=order.pk)
    from django.views.generic.detail import DetailView
from .models import Order
"""

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_price = sum(item.price for item in order.items.all())
            order.save()
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'menu/create_order.html', {'form': form})

class OrderDetailView(DetailView):
    model = Order
    template_name = 'menu/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

"""These are two Django class-based views for displaying
 the list of items in a particular category and the details
   of a single item."""
class ItemsListView(ListView):
    #this is a string that specifies the name of the template file t
    # that the view will use to rener HTML for the page

    template_name = 'menu/item_list.html'
    #this is the django model that 
    # the view will use to fetch the data to display on the page
    model = Item
    # This is the name of the context variable that 
    # the view will use to store the data to display on the page.
    context_object_name = "item_list"
    #this method is responsible for fatching the quryset if items that the view will display on the page 
    #it does this by retriving the category from the url parameters and then filteriing the items by that category

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs["category"])
        return Item.objects.filter(category=category)
# This method is responsible for fetching the queryset of items that the view will display on the page.
#  It does this by retrieving the category from the URL parameters and then filtering the items by that category.
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(slug=self.kwargs['category'])
        return context


class ItemsDetailsView(DetailView):
    template_name = 'menu/item_detail.html'
    model = Item
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context
