from django.urls import path
from .import views, auth_views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('updateOrder/', views.updateOrder, name='updateOrder'),
    path('processOrder/', views.processOrder, name='processOrder'),

    path('get_searched_product/', views.get_searched_product, name='get_searched_product'),

    # authentication routes
    path('loginUser/', auth_views.loginUser, name="loginUser"),
    path('registerUser/', auth_views.registerUser, name="registerUser"),
    path('logoutUser/', auth_views.logoutUser, name="logoutUser")
]