from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.product_list , name="product_list"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('signup/',views.views_signup if hasattr(views,'views_signup') else views.signup, name='signup'),
    path('login/' , auth_views.LoginView.as_view(template_name = 'store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page= 'product_list'),name='logout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/decrease/<int:product_id>/', views.decrease_cart_item, name='decrease_cart_item'),
    path('cart/remove/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_success/', views.order_success, name='order_success'),
    path('my_orders/', views.my_orders, name='my_orders'),
]
if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)