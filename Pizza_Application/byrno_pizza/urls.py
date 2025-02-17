from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('create_pizza', views.create_pizza, name='create_pizza'),
    path('order_details/<int:order_id>', views.order_details, name='order_details'),
    path('order_confirmation/<int:order_id>', views.order_confirmation, name='order_confirmation'),
    path('place_order/<int:pizza_id>/', views.place_order, name='place_order'),
]

