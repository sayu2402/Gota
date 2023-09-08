from . import views
from django.urls import path

urlpatterns = [
    path('admin_product_list',views.admin_product_list, name='admin_product_list'),
    path('add_product', views.add_product, name='add_product'),
    path('product_delete/<slug:product_slug>/', views.product_delete, name='product_delete'),
    path('', views.store, name='store'),
    path('product_edit/<slug:product_slug>/', views.product_edit, name='product_edit'),
    path('category/<slug:category_slug>/', views.store, name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('variations_list/', views.variation_list, name='variation_list'),
    path('update_is_active/<int:variation_id>/', views.update_is_active, name='update_is_active'),
    path('add_product_offer/', views.add_product_offer, name='add_product_offer'),
    path('admin/edit_offer/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('admin/delete_offer/<int:offer_id>/', views.delete_offer, name='delete_offer'),
    path('search',views.search,name='search'),
]