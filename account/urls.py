from . import views
from django.urls import path

urlpatterns = [
     path('loginpage', views.loginpage, name='loginpage'),
     path('signup',views.signup, name='signup'),
     path('logoutpage',views.logoutpage, name='logoutpage'),
     path ('user_list', views.user_list, name='user_list'),
     path('user/block/<int:user_id>/', views.block_user, name='block_user'),
     path('user/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
     path('otp_validation/<str:email>/', views.otp_validation, name='otp_validation'),
]
