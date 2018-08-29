from django.conf.urls import url

from app_libros import views

urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
    # url(r'^new_book$', views.libro_view, name='libro_crear'),
    url(r'^new_periodo$', views.crear_periodo_view, name='crear_periodo'),
    url(r'^ver_periodos$', views.ver_periodos_view, name='ver_periodos'),
    url(r'^ver_roles/(?P<pk>\d+)$', views.ver_roles_view, name='ver_roles'),
    url(r'^ver_detalle_rol/(?P<pk>\d+)$', views.ver_detalle_rol_view, name='ver_detalle_rol'),


    url(r'^persona/delete/$', views.delete_persona_ajax.as_view(), name='del_persona'),


    url(r'^roles_pago/list/$', views.listar_rolesPago.as_view(), name='listar_rolesPago'),
    url(r'^roles_pago/load/$', views.cargar_rolesPago_ajax, name='cargar_rolesPago'),
    url(r'^roles_pago/delete/$', views.remover_rolesPago_ajax, name='remover_rolesPago'),
    url(r'^roles_pago/create/$', views.crear_rolPago_ajax, name='crear_rolesPago'),
]
