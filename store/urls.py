from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # 👈 Add this line
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('my-orders/', views.my_orders_view, name='my_orders'),
    path('my-orders/', views.my_orders, name='my_orders'), 
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/', views.view_cart, name='cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),
   path('product/<int:product_id>/', views.product_detail, name='product_detail'),


 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

  # 👈 This is your homepage
