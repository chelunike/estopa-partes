"""estopaparts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.register, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    # Listado de productos
    path('my-products/', views.products_list, name='my-products'),
    path('products/', views.product_seller, name='products'),
    path('products/remove/<int:id>', views.product_remove, name='product-remove'),
    path('products/edit/<int:id>', views.product_edit, name='product-edit'),
    path('product/<int:id>', views.product_single, name='product'),

    # Listado de pedidos
    path('orders/', views.orders, name='orders'),
    path('products/orders/', views.orders_seller, name='orders-seller'),
    path('order/pay/<int:id>', views.pay_order, name='pay-order'),
    path('order/remove/<int:id>', views.order_remove, name='order-remove'),
    path('order/<int:order_id>/remove/<int:product_id>', views.order_remove_product, name='order-remove-product'),
    
    # Vistas del website
    path('mostrarProductos', views.productos, name='mostrarProductos'),
    path('carrito', views.carrito, name='carrito'),
    path('tramitar', views.tramitar, name='tramitar'),
    path('compra', views.compra, name='compra'),
    
    # Vista de administrador
    path('valoraciones/', views.gestionValoraciones, name='valoraciones'),
    path('usuarios/', views.gestionUsuarios, name='usuarios')
]


