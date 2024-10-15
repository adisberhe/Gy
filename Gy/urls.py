
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('GY_app.urls'),name='index'),

    
    #path('accounts/', include('accounts.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    
]