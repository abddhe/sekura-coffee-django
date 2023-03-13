from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about-us', views.AboutUsView.as_view(), name="about_us"),
    path('contact-us', views.ContactUsView.as_view(), name="contact_us"),
    path('orders', views.OrderListView.as_view(), name="orders"),
    path('menu/<slug:category>', views.ItemsListView.as_view(), name="item_list"),
    path('menu/<slug:category>/<int:pk>', views.ItemsDetailsView.as_view(), name="item_detail"),
    path('orders/create', views.order_create, name="order_create"),
    path('orders/make-order', views.order_make, name="order_make"),
    path('orders/update', views.order_update, name="order_update"),
<<<<<<< HEAD
  
    path('orders/add_comment/<int:pk>', add_comment, name='add_comment'),
=======
    path('orders/<int:pk>/comments', views.comment_listing, name="comment_list"),
    path('orders/<int:pk>/comments/create', views.comment_create, name="comment_create"),

>>>>>>> 88b879521a881e183c47df9bdd69bb6a63ba0e77
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
