from django.db import models
from app_prestamo.models import Persona

TIPO_DESCUENTO = (("mensual", "Mensual"), ("quincenal", "Quincenal"))
MES_PERIODO = (
    ("ENERO", "ENERO"), ("FEBRERO", "FEBRERO"),
    ("MARZO", "MARZO"), ("ABRIL", "ABRIL"),
    ("MAYO", "MAYO"), ("JUNIO", "JUNIO"),
    ("JULIO", "JULIO"), ("AGOSTO", "AGOSTO"),
    ("SEPTIEMBRE", "SEPTIEMBRE"), ("OCTUBRE", "OCTUBRE"),
    ("NOVIEMBRE", "NOVIEMBRE"), ("DICIEMBRE", "DICIEMBRE"))

# Create your models here.
# class Author(models.Model):
#     nombre = models.CharField(max_length=300, verbose_name="NOMBRES")
#     fecha_nac = models.DateField(verbose_name="FECHA NACIMIENTO")
#     fecha_mue = models.DateField(verbose_name="FECHA MUERTE")
#
#     def __str__(self):
#         return self.nombre
#
# class Book(models.Model):
#     codigo = models.CharField(max_length=50, verbose_name="CÓDIGO")
#     titulo = models.CharField(max_length=300, verbose_name="TÍTULO")
#     resumen = models.CharField(max_length=500, verbose_name="RESUMEN")
#     imprenta = models.CharField(max_length=200, verbose_name="IMPRENTA")
#     nro_pag = models.IntegerField(default=0, verbose_name="NRO. PÁGINAS")
#     fecha_pub = models.DateField(verbose_name="FECHA PUBLICACIÓN")
#     #Una persona puede pedir varios libros (1..*)
#     persona = models.ForeignKey(Persona, null=True, blank=True, on_delete=models.CASCADE)
#     #Un libro puede tener muchos autores y un autor muchos libros
#     autor = models.ManyToManyField(Author)
#
#     def __str__(self):
#         return self.titulo

class Periodo_Rol(models.Model):
    mes = models.CharField(verbose_name="Mes", max_length=15, choices=MES_PERIODO)
    anio = models.CharField(verbose_name="Año", max_length=4, help_text="Ejemplo: '2010'")
    max_dias = models.IntegerField(default=30)
    emitido = models.BooleanField(verbose_name="Completado", default=False)
    fecha_emision = models.DateTimeField(auto_now_add=True)#Fecha de creado el Rol

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self):
        return u"{0} {1}".format(self.mes, str(self.anio))

class Rol_Pago(models.Model):
    codigo = models.CharField(verbose_name="Rol de Pagos", null=True, blank=True, max_length=255)
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, verbose_name="Partida", blank=False, null=True,
                                related_name='partida_rol')

    periodo_rol = models.ForeignKey(Periodo_Rol, on_delete=models.CASCADE, verbose_name='Periodo')

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Rol de Pago'
        verbose_name_plural = 'Roles de Pago'

    def __str__(self):
        return u'{0}'.format(self.persona)

class Ingreso(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=255, unique=True, null=False)
    descripcion = models.TextField(verbose_name="Descripción")
    activo = models.BooleanField(verbose_name="Activo", default=True, help_text="Si es activo para todos los meses")

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return u'{0}'.format(self.nombre)

class Descuento(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=255, unique=True, null=False)
    descripcion = models.TextField(verbose_name="Descripción")
    activo = models.BooleanField(verbose_name="Activo", default=True, help_text="Si es activo para todos los meses")
    fijo = models.BooleanField(verbose_name="Fijo", default=False, help_text="Si es fijo para todos los meses")
    tipo = models.CharField(verbose_name="Tipo Descuento", max_length=100, help_text="Información Histórica",
                            choices=TIPO_DESCUENTO)  # pago quincenal o mensual (para historial)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return u'{0}'.format(self.nombre)

class Ingreso_Rol(models.Model):
    rol_pago = models.ForeignKey(Rol_Pago, on_delete=models.PROTECT, verbose_name="Rol de Pago")
    ingreso = models.ForeignKey(Ingreso, on_delete=models.PROTECT, verbose_name="Ingreso")
    valor = models.DecimalField(verbose_name="Valor ingreso", max_digits=9, decimal_places=2, default=0.0)

class Descuento_Rol(models.Model):
    rol_pago = models.ForeignKey(Rol_Pago, on_delete=models.PROTECT, verbose_name="Rol de Pago", blank=True, null=True)
    descuento = models.ForeignKey(Descuento, on_delete=models.PROTECT, verbose_name="Descuento", blank=True, null=True)
    valor = models.DecimalField(verbose_name='Valor Descuento', max_digits=9, decimal_places=2, default=0.0,
                                blank=True)

class Presupuestacion_Partidas(models.Model):
    numero = models.CharField(verbose_name="Número", max_length=255)
    nombre = models.CharField(verbose_name="Nombre", max_length=255)
    activa = models.BooleanField(verbose_name="Cuenta Activa", default=False)
    # tipo = models.CharField(verbose_name="Tipo", choices=TIPO_CUENTAS, max_length=255)
    orden = models.IntegerField(verbose_name="Orden", blank=True, null=True)
    imprimir = models.BooleanField(verbose_name="Imprimir", default=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return u'{0}'.format(self.nombre)


