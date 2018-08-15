from django.conf.urls import url

from app_libros import views

urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
    url(r'^new_book$', views.libro_view, name='libro_crear'),
    url(r'^new_periodo$', views.crear_periodo_view, name='crear_periodo'),
    # url(r'^ver_periodos$', views.periodo_detalle_view, name='periodo_ver'),
    # url(r'^ver_roles/(?P<pk>\d+)$', views.rol_detalle_view, name='rol_ver'),
    # url(r'^ver_descuentos/(?P<pk>\d+)$', views.descuento_view, name='descuento_ver'),
]
