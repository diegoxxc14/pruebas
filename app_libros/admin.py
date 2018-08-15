from django.contrib import admin
from app_libros.models import Author, Book, Periodo_Rol, Rol_Pago, Descuento, Descuento_Rol
# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Periodo_Rol)
admin.site.register(Rol_Pago)
admin.site.register(Descuento)
admin.site.register(Descuento_Rol)