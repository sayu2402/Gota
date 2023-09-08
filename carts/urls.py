from . import views
from django.urls import path

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_coupon/<int:cart_id>/', views.remove_coupon, name='remove_coupon'),
    path('manage-coupons/', views.manage_coupons, name='manage_coupons'),
    path('edit-coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('delete-coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
]