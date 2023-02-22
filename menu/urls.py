from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about-us', views.AboutUsView.as_view(), name="about_us"),
    path('contact-us', views.ContactUsView.as_view(), name="contact_us"),
    path('orders', views.OrderListView.as_view(), name="orders"),
    path('menu/<slug:category>', views.ItemsListView.as_view(), name="item_list"),
    path('menu/<slug:category>/<int:pk>', views.ItemsDetailsView.as_view(), name="item_detail"),
]
