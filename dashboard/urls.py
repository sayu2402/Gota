from . import views
from django.urls import include, path

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('adminlogout', views.adminlogout, name='adminlogout'),

    path('add_address/', views.add_address, name='add_address'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('deleteaddress/<int:delete_id>', views.deleteaddress, name='deleteaddress'),
    path('edit_address/<int:edit_id>', views.edit_address, name='edit_address'),
    path('add_new_adress', views.add_new_adress, name='add_new_adress'),
    path('checkout_confirmation/', views.checkout_confirmation, name='checkout_confirmation'),
    path('edit_address_checkout/<int:edit_id>/', views.edit_address_checkout, name='edit_address_checkout'),
    path('delete_address_checkout/<int:delete_id>/', views.delete_address_checkout, name='delete_address_checkout'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('generate_pdf/<int:order_id>/', views.generate_pdf, name='generate_pdf'),
]