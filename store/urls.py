from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.product_list , name="product_list"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

]
if settings.DEBUG:
    from django.conf import settings
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)