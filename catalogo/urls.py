from django.urls import path

from django.contrib.auth import views as auth_views

from . import views


app_name = 'catalogo'


urlpatterns = [


    path('login/', auth_views.LoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/login/', views.custom_login, name='login_custom'),



    path('', views.inicio, name='inicio'),

    path('contacto/', views.contacto, name='contacto'),



    path('carrito/', views.ver_carrito, name='ver_carrito'),

    path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),

    path('carrito/eliminar/<int:producto_id>/<int:eliminar_todo>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path('catalogo/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito_alt'),

    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),

    path('actualizar_carrito/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),



    path('confirmar-compra/', views.confirmar_compra, name='confirmar_compra'),

    path('compra-exitosa/<int:pedido_id>/', views.compra_exitosa, name='compra_exitosa'),

    path('checkout/confirmar/', views.confirmar_compra, name='confirmar_compra_alt'),

    path('orden-exitosa/', views.orden_exitosa, name='orden_exitosa'),



    path('catalogo/', views.catalogo, name='catalogo'),

    path('catalogo/listar/', views.catalogo_listar, name='catalogo_listar'),



    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),



    path('buscar/', views.buscar, name='buscar'),



    path('procesar_contacto/', views.procesar_contacto, name='procesar_contacto'),

    path('procesar_envio/', views.procesar_envio, name='procesar_envio'),

    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),



    path('finalizar_compra/', views.checkout, name='checkout'),

    path('generar_boleta/<str:nombre>/<str:total>/<str:productos>/<str:metodo_pago>/<str:alias>/', views.generar_boleta, name='generar_boleta'),



    path('carga-masiva/', views.carga_masiva, name='carga_masiva'),

    path('productos/', views.listar_productos, name='listar_productos'),



    path('agregar/', views.agregar_producto, name='agregar_producto'),

    path('actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),

    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),

    path('eliminar/', views.eliminar_productos, name='eliminar_productos'),
    path('productos/marcar/', views.marcar_productos, name='marcar_productos'),
    path('productos/deshacer/', views.deshacer_ultima_accion, name='deshacer_ultima_accion'),



    path('crear_orden/', views.crear_orden, name='crear_orden'),

    path('confirmacion_orden/<int:orden_id>/', views.confirmacion_orden, name='confirmacion_orden'),

    path('ordenView/', views.vista_orden, name='vista_orden'),



    path('politicas-envio/', views.politicas_envio, name='politicas_envio'),

    path('confirmar-envio/', views.confirmar_envio, name='confirmar_envio'),

]
