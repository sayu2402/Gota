from . import views
from django.urls import path

urlpatterns = [
    path('admin_categories',views.admin_categories, name='admin_categories'),
    path('add_categories', views.add_categories, name='add_categories'),
    path('category_detail/<int:category_id>/', views.category_detail, name='category_detail'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('add_category_offer/', views.add_category_offer, name='add_category_offer'),
    path('admin/edit_category_offer/<int:offer_id>/', views.edit_category_offer, name='edit_category_offer'),
    path('admin/delete_category_offer/<int:offer_id>/', views.delete_category_offer, name='delete_category_offer'),
]