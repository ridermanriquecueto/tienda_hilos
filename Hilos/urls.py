from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),  # Página principal del sitio web
    path('catalogo/', include('catalogo.urls')),  # Aquí están los productos
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  
]
