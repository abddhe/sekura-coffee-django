from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView)
from .models import (Category, Item)
from datetime import datetime


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


class ItemsListView(ListView):
    template_name = 'menu/item_list.html'
    model = Item
    context_object_name = "item_list"

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs["category"])
        return Item.objects.filter(category=category)

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
