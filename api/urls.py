from django.urls import path
from api import base_views, expense_views, order_views, product_views, stock_views

urlpatterns = [
    path('users/', base_views.users_view),
    path('user/<int:id>/', base_views.user_view),

    path('categories/', product_views.category_list, name='category_list'),
    path('categories/<int:pk>/', product_views.category_detail, name='category_detail'),
    path('products/', product_views.product_list, name='product_list'),
    path('products/<int:pk>/', product_views.product_detail, name='product_detail'),

    path('orders/', order_views.order_list, name='order_list'),
    path('orders/<int:pk>/', order_views.order_detail, name='order_detail'),
    path('order-items/', order_views.order_item_list, name='order_item_list'),
    path('order-items/<int:pk>/', order_views.order_item_detail, name='order_item_detail'),

    path('stocks/', stock_views.stock_list, name='stock_list'),
    path('stocks/<int:pk>/', stock_views.stock_detail, name='stock_detail'),

    path('expenses/', expense_views.expense_list, name='expense_list'),
    path('expenses/<int:pk>/', expense_views.expense_detail, name='expense_detail'),
]