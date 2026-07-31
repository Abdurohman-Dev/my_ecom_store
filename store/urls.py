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
    path('logout/', auth_views.LogoutView.as_view(next_page= 'producy_list'),name='logout'),
]
if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)