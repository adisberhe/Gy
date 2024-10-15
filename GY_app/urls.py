
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *



urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('shop/', shop, name='shop'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('mycart/', cart, name='mycart'),
    path('checkout/', place_order, name='checkout'),
    path('product/<int:product_id>/', product, name='product'),
    path('contact/', contact, name='contact'),
]



if settings.DEBUG:  # Only serve media files in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)