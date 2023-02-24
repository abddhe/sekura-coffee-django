from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.views.generic import (CreateView, UpdateView, TemplateView, ListView, DetailView)
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import (Category, Item, Order, Table, OrderItem)
from datetime import datetime
from django.urls import reverse_lazy
from menu.forms import OrderForm
from django.http import (Http404, HttpRequest, JsonResponse)
from django.core.exceptions import ObjectDoesNotExist


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['order_list'] = Order.objects.filter(table_id=1, order_accept=False)
        return context


class ItemsListView(ListView):
    """These are two Django class-based views for displaying
         the list of items in a particular category and the details
           of a single item."""
    # this is a string that specifies the name of the template file t
    # that the view will use to render HTML for the page

    template_name = 'menu/item_list.html'
    # this is the django model that
    # the view will use to fetch the data to display on the page
    model = Item
    # This is the name of the context variable that 
    # the view will use to store the data to display on the page.
    context_object_name = "item_list"

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


@csrf_exempt
def order_create(request: HttpRequest):
    try:
        if request.method == 'POST':
            item = get_object_or_404(Item, pk=int(request.POST['itemId']))
            if "order" not in request.session:
                request.session['order'] = Order.objects.create(table_id=1).pk
                request.session.save()
            order = Order.objects.filter(pk=request.session['order']).exists()
            if not order:
                order = Order.objects.create(table_id=1)
                request.session['order'] = order.pk
                request.session.save()
            else:
                order = Order.objects.get(pk=request.session['order'])
            order_items = OrderItem.objects.filter(order=order, item=item).exists()
            if not order_items:
                print()
                OrderItem.objects.create(order=order, item=item)
            else:
                order_items = OrderItem.objects.filter(order=order, item=item).first()
                order_items.count += 1
                order_items.save()
            return JsonResponse({"status": 'success', "message": "Item has been added"})
        return redirect(reverse_lazy('home'))
    except ObjectDoesNotExist:
        return JsonResponse({"status": 'error', "message": "This item is not exists"})
    except Http404:
        return JsonResponse({"status": 'error', "message": "This item is not exists"})
    except ValueError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"})


@csrf_exempt
def order_make(request: HttpRequest):
    try:
        if request.method == "POST":
            order = get_object_or_404(Order, pk=int(request.POST['order']))
            if order.table_id != 1:
                raise ValueError()
            order.ordered = True
            order.save()
            # here must be notification firebase
            return JsonResponse({"status": 'success', "message": "Order has been sent to chief",
                                 "html": ' <button type="button" class="btn order-cancel w-100 btn-submit">Cancel</button>'})
        return redirect(reverse_lazy('home'))
    except ObjectDoesNotExist:
        return JsonResponse({"status": 'error', "message": "This order is not exists"})
    except Http404:
        return JsonResponse({"status": 'error', "message": "This order is not exists"})
    except ValueError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"})


@csrf_exempt
def order_update(request: HttpRequest):
    try:
        if request.method == "POST":
            operation_type = str(request.GET['op']).strip().lower()
            request.POST.get('order')
            if operation_type == "order-cancel":
                order = Order.objects.get(pk=int(request.POST['order']))
                order.delete()
                return JsonResponse(
                    {'status': 'success', 'operation': "order-cancel", 'message': "Order has been canceled"})
            request.POST.get('item')
            order_item = get_object_or_404(OrderItem, order_id=int(request.POST['order']),
                                           item_id=int(request.POST['item']))
            if operation_type == 'count-plus':
                order_item.count += 1
                order_item.save()
                return JsonResponse(
                    {'status': 'success', 'operation': "plus", 'message': "Order has been updated", "data": {
                        "count": order_item.count
                    }})
            elif operation_type == 'count-minus':
                if order_item.count == 1:
                    order_item.delete()
                    if order_item.order.orderitem_set.count() == 0:
                        order_item.order.delete()
                        return JsonResponse(
                            {'status': 'success', 'operation': "order-cancel", 'message': "Order has been canceled"})
                    return JsonResponse(
                        {'status': 'success', 'operation': "item-cancel",
                         'message': "Item has been removed from your order"})
                if order_item.count > 1:
                    order_item.count -= 1
                    order_item.save()
                    return JsonResponse(
                        {'status': 'success', 'operation': "minus", 'message': "Order has been updated", "data": {
                            "count": order_item.count
                        }})
            elif operation_type == "item-cancel":
                order_item.delete()
                if order_item.order.orderitem_set.count() == 0:
                    order_item.order.delete()
                    return JsonResponse(
                        {'status': 'success', 'operation': "order-cancel", 'message': "Order has been canceled"})
                return JsonResponse(
                    {'status': 'success', 'operation': "item-cancel",
                     'message': "Item has been removed from your order"})
        return redirect(reverse_lazy('home'))
    except ObjectDoesNotExist:
        return JsonResponse({"status": 'error', "message": "This order is not exists"})
    except Http404:
        return JsonResponse({"status": 'error', "message": "order item is not exists"})
    except ValueError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"})
    except KeyError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"})
