import json
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.views.generic import (CreateView, UpdateView, TemplateView, ListView, DetailView)
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import (Category, Item, Comment, Order, Table, OrderItem, Notification)
from datetime import datetime
from django.urls import reverse_lazy
from menu.forms import CommentForm
from django.http import (Http404, HttpRequest, JsonResponse, HttpResponse)
from django.core.exceptions import ObjectDoesNotExist
from menu.utils import generate_token_by_id
from django.core.paginator import Paginator, EmptyPage

# this view returns the 'menu/index.html' template with all the Category objects as context data.
class HomeView(TemplateView):
        #The template_name attribute is set to 'menu/index.html', which indicates the template that will be used to render the view.

    template_name = 'menu/index.html'
#The get_context_data method is overridden to add extra data to the context that will be used in the template. 
# In this case, it adds all the Category objects to the context under the key 'categories'.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AboutUsView(HomeView):
    template_name = 'menu/about-us.html'


class ContactUsView(HomeView):
    template_name = 'menu/contact-us.html'


class OrderListView(HomeView):
    #It extends the HomeView class and overrides the get_context_data method to add an additional context data named order_list.    

    template_name = 'menu/orders.html'
 #he order_list data is a queryset of Order objects filtered by table_id=1, canceled=False, 
    # and created_at__date=datetime.today() (orders for today). The results are sorted in descending order based on the created_at field.
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['order_list'] = Order.objects.filter(table_id=1, canceled=False,
                                                     created_at__date=datetime.today()).order_by('-created_at')
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
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = Category.objects.get(slug=self.kwargs['category'])

        # Get the page number from the URL parameters
        page_number = self.request.GET.get('page') or 1
        print(context['item_list'])
        # Paginate the queryset
        paginator = Paginator(context['item_list'], 3)
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            page_obj = paginator.page(1)

        # Update the context with the paginated items and the page object
        context['item_list'] = page_obj.object_list
        context['page_obj'] = page_obj

        return context


class ItemsDetailsView(DetailView):
    template_name = 'menu/item_detail.html'
    model = Item
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        return context
#This code defines a view function order_create that allows users to add items to an order.
#The function is marked with @csrf_exempt, which disables CSRF protection for this view.

@csrf_exempt
 # When a user submits a POST request to this view, 
    # the function first tries to retrieve the Item object associated with the submitted itemId from the request's POST data.
    # If the item does not exist, the function returns a JSON response indicating an error.
def order_create(request: HttpRequest):
    try:
        #If the item exists, the function then checks whether an order is already associated with the user's session. 
        # If an order does not exist, a new order is created and the order's primary key is saved to the user's session. 
        # If an order does exist, the function retrieves it using the primary key stored in the user's session.
        if request.method == 'POST':
            #If the retrieved order has already been marked as "ordered" (i.e., the user has submitted the order for processing), 
            # a new order is created and the order's primary key is saved to the user's session.
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
             #The function then checks whether the specified item is already associated with the order.
                #  If it is not, a new OrderItem object is created and associated with the order and the specified item.
                #  If it is, the function increments the count of the existing OrderItem object.

            if order.ordered:
                order = Order.objects.create(table_id=1)
                request.session['order'] = order.pk
                request.session.save()

            order_items = OrderItem.objects.filter(order=order, item=item).exists()
            if not order_items:
                OrderItem.objects.create(order=order, item=item)
            else:
                order_items = OrderItem.objects.filter(order=order, item=item).first()
                order_items.count += 1
                order_items.save()
            return JsonResponse({"status": 'success', "message": "Item has been added"})
        return redirect(reverse_lazy('home'))
     #Finally, the function returns a JSON response indicating success and a message indicating that the item has been added to the order.
                #  If the request method is not POST, the function redirects the user to the homepage.
                #  If an error occurs during processing, the function returns a JSON response indicating the error.
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
                                 'token': order.user_token,
                                 "html": '<button type="button" class="btn mb-2 comment w-100 btn-submit">Order Comment</button><button type="button" class="btn order-cancel w-100 btn-submit">Cancel</button>'})
        return redirect(reverse_lazy('home'))
    except ObjectDoesNotExist:
        return JsonResponse({"status": 'error', "message": "This order is not exists"})
    except Http404:
        return JsonResponse({"status": 'error', "message": "This order is not exists"})
    except ValueError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"})
    except KeyError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"})


@csrf_exempt
def order_update(request: HttpRequest):
    try:
        if request.method == "POST":
             #It starts by checking if the request method is POST, 
        # and then it reads the operation type from the GET parameter 'op' and the order and item IDs from the POST parameters.
            operation_type = str(request.GET['op']).strip().lower()
             #If the operation type is 'order-cancel',
            #  the function deletes the entire order and returns a success message with the operation type 'order-cancel'
            #  and a message indicating that the order has been canceled.
            if operation_type == "order-cancel":
                order = Order.objects.get(pk=int(request.POST['order']))
                order.delete()
                return JsonResponse(
                    {'status': 'success', 'operation': "order-cancel", 'message': "Order has been canceled"})
            order_item = get_object_or_404(OrderItem, order_id=int(request.POST['order']),
                                           item_id=int(request.POST['item']))
            #If the operation type is 'count-plus', 
            #  the function adds one to the count of the given order item and returns a success message with the operation type 'plus',
            #  a message indicating that the order has been updated, and the updated count.
            if order_item.order.ordered:
                raise ValueError()
            if operation_type == 'count-plus':
                order_item.count += 1
                order_item.save()
                return JsonResponse(
                    {'status': 'success', 'operation': "plus", 'message': "Order has been updated", "data": {
                        "count": order_item.count
                    }})
             #If the operation type is 'count-minus', 
            # the function subtracts one from the count of the given order item.
            #  If the count becomes zero, the order item is deleted. If the order has no more items after the deletion, 
            # the entire order is also deleted. The function then returns a success message with the operation type 'minus' or 'item-cancel', 
            # a message indicating that the order has been updated or the item has been removed, and the updated count (if applicable).
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
                 #f the operation type is 'item-cancel', 
                # the function deletes the given order item. If the order has no more items after the deletion,
                #  the entire order is also deleted. The function then returns a success message with the operation type 'item-cancel',
                #  a message indicating that the item has been removed, and the updated count (if applicable).
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
   #If any exceptions occur during the function, such as an ObjectDoesNotExist or Http404 error, a JSON response is returned with a status of 'error' and an appropriate error message.
     #  If a KeyError or ValueError occurs, indicating that the request parameters were invalid, a similar error response is returned.
    except ObjectDoesNotExist:
        return JsonResponse({"status": 'error', "message": "This order is not exists"}, status=404)
    except Http404:
        return JsonResponse({"status": 'error', "message": "order item is not exists"}, status=404)
    except ValueError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"}, status=500)
    except KeyError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"}, status=500)

#This is a Django view function that handles a GET request for retrieving a list of comments associated with an order
#The function takes in a HttpRequest object and an integer pk as parameters, where pk is the primary key of the order.
def comment_listing(request: HttpRequest, pk: int):
    try:
                #Inside the function, it first checks if the request method is GET.
        #  If not, it redirects the user to the home page using the reverse_lazy() function.
        if request.method != 'GET':
            return redirect(reverse_lazy('home'))
         #Next, the function creates a copy of the request.
        order = get_object_or_404(Order, pk=pk)
         #Next, it queries the Comment model to get all comments associated with the order using Comment.objects.filter(order=order). 
        # The values() function is called on the resulting queryset to convert it into a list of dictionaries
        comments = Comment.objects.filter(order=order).values()
       # If there are no comments, data is set to False. Otherwise, data is set to the list of comments.
        if comments.count() == 0:
            data = False
        else:
            data = list(comments)
            #Finally, a JSON response is returned with a status key set to "success" and a data key set to the data variable.
        #  If there is an error, an appropriate error message and status code are returned.
        return JsonResponse({"status": "success", "data": data}, safe=False)
    except Http404:
        return JsonResponse({"status": 'error', "message": "This order is not exists"}, status=404)
    except ValueError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"}, status=500)
    except KeyError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"}, status=500)


@csrf_exempt
def comment_create(request, pk: int):
     #This function first checks if the request method is not POST, and if it is not, then it redirects to the home page.
    try:
        if request.method != 'POST':
            return redirect(reverse_lazy('home'))
         #Next, the function creates a copy of the request.
        post = request.POST.copy()
         # POST data, gets the Order object with the given primary key (pk), 
        order = get_object_or_404(Order, pk=pk)
         # adds the order ID to the POST data,
        if order.canceled:
            return JsonResponse({"status": "error", 'message': 'This order was canceled', })
        post['order'] = order.pk
         # and creates an instance of the CommentForm with the modified POST data.
        form = CommentForm(data=post)
         #If the form is valid, the function saves the comment object to the database,
        if form.is_valid():
            #  gets all the comments related to the order using Comment.objects.filter(order_id=pk).
             # values(), converts the queryset to a list and returns it as JSON response.
            form.save()
            comments = Comment.objects.filter(order_id=pk).values()
            data = list(comments)
            return JsonResponse({"status": "success", 'message': 'The comment was added successfully', "data": data})
        return JsonResponse({"status": 'error', "errors": form.errors}, status=404)
    except Http404:
        return JsonResponse({"status": 'error', "message": "This order is not exists"}, status=404)
    except ValueError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"}, status=500)
    except KeyError:
        return JsonResponse({"status": "error", 'message': "Please don't play on site"}, status=500)
