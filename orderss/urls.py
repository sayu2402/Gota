from . import views
from django.urls import path

urlpatterns = [
    path('place_order', views.place_order, name='place_order'),
    path('order_list', views.order_list, name='order_list'),
    path('cancel_order/<int:order_id>',views.cancel_order, name='cancel_order'),
    path('update_order_status/<int:order_id>',views.update_order_status, name='update_order_status'),
    path('order/user_order_detail', views.user_order_detail, name='user_order_detail'),
    path('cancel_order_user/<int:order_id>/', views.cancel_order_user, name='cancel_order_user'),
    path('payment',views.payment,name='payment'),
    path('admin_order_details/<int:order_id>/', views.admin_order_details, name='admin_order_details'),
    path('get_order_details/<int:order_id>/', views.get_order_details, name='get_order_details'),
    path('user_view_order/<int:order_id>/', views.user_view_order, name='user_view_order'),

]