from django.urls import path
from .import views 


urlpatterns = [
    
    path('', views.home_page, name='home_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('register_page/', views.register_page, name='register_page'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('shipping_info/', views.shipping_info, name='shipping_info'),
    path('create_product/', views.create_product, name='create_product'),
    
]
