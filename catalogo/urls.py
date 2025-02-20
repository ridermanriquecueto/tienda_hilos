from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import confirmar_compra, orden_exitosa


urlpatterns = [
    # Autenticación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', views.custom_login, name='login'),

    # Páginas principales
    path('', views.inicio, name='inicio'),
    path('productos/', views.listar_productos, name='listar_productos'),
    path('contacto/', views.contacto, name='contacto'),

    # Carrito de compras
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('carrito/eliminar/<int:producto_id>/<int:eliminar_todo>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar_carrito/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),

    # Confirmación de compra
    path('confirmar-compra/', views.confirmar_compra, name='confirmar_compra'),
    path('compra-exitosa/<int:pedido_id>/', views.compra_exitosa, name='compra_exitosa'),

    # Catálogo
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/listar/', views.catalogo_listar, name='catalogo_listar'), 
    path('catalogo/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),

    # Detalle de productos
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Búsqueda
    path('buscar/', views.buscar, name='buscar'),

    # Procesos de contacto, envío y pago
    path('procesar_contacto/', views.procesar_contacto, name='procesar_contacto'),
    path('procesar_envio/', views.procesar_envio, name='procesar_envio'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),

    # Finalizar compra y generar boleta
    path('finalizar_compra/', views.checkout, name='checkout'),
    path('generar_boleta/<str:nombre>/<str:total>/<str:productos>/<str:metodo_pago>/<str:alias>/', views.generar_boleta, name='generar_boleta'),

    # Carga masiva de productos
    path('carga-masiva/', views.carga_masiva, name='carga_masiva'),

    # Agregar y actualizar productos
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),

    # Eliminar productos
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # Confirmación de orden
    path('crear_orden/', views.crear_orden, name='crear_orden'),
    path('confirmacion_orden/<int:orden_id>/', views.confirmacion_orden, name='confirmacion_orden'),

    # Vista para ordenar
    path('ordenView/', views.vista_orden, name='vista_orden'),

    # Políticas de envío
    path('politicas-envio/', views.politicas_envio, name='politicas_envio'),


    path("checkout/confirmar/", confirmar_compra, name="confirmar_compra"),
  
    path("orden-exitosa/", orden_exitosa, name="orden_exitosa"),
]
