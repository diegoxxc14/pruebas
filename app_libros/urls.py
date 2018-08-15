from django.conf.urls import url

from app_libros import views

urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
    # url(r'^new_book$', views.libro_view, name='libro_crear'),
    url(r'^new_periodo$', views.crear_periodo_view, name='crear_periodo'),
    url(r'^ver_periodos$', views.ver_periodos_view, name='ver_periodos'),
    url(r'^ver_roles/(?P<pk>\d+)$', views.ver_roles_view, name='ver_roles'),
    url(r'^ver_detalle_rol/(?P<pk>\d+)$', views.ver_detalle_rol_view, name='ver_detalle_rol'),
]
