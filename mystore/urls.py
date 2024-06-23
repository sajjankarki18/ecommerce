from django.urls import path
from .import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('updateOrder/', views.updateOrder, name='updateOrder'),
    path('processOrder/', views.processOrder, name='processOrder')
]