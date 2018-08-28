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

class Periodo_Rol(models.Model):
    mes = models.CharField(verbose_name="Mes", max_length=15, choices=MES_PERIODO)
    anio = models.CharField(verbose_name="Año", max_length=4, help_text="Ejemplo: '2010'")
    max_dias = models.IntegerField(default=30)  #Información histórica
    emitido = models.BooleanField(verbose_name="Completado", default=False)

    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

    def __str__(self):
        return u"{0} {1}".format(self.mes, str(self.anio))


class Rol_Pago(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name="Partida", blank=False, null=True,
                                related_name='partida_rol') #Temporal, equivalente a la partida
    periodo_rol = models.ForeignKey(Periodo_Rol, on_delete=models.CASCADE, verbose_name='Periodo')

    dias_trabajados = models.IntegerField(verbose_name="Días trabajados", default=30)
    aporte_patronal = models.DecimalField(verbose_name="Aporte Patronal", max_digits=10, decimal_places=2, default=0.0)
    total_ingresos = models.DecimalField(verbose_name="Total ingresos", max_digits=10, decimal_places=2, default=0.0)
    total_descuentos = models.DecimalField(verbose_name="Total descuentos", max_digits=10, decimal_places=2, default=0.0)
    total_pagar = models.DecimalField(verbose_name="Total a pagar", max_digits=10, decimal_places=2, default=0.0)

    fecha_emision = models.DateTimeField(auto_now_add=True)  # Fecha de creado el Rol
    fecha_edicion = models.DateTimeField(auto_now=True) #Fecha de última edición del Rol

    class Meta:
        ordering = ['-pk']
        verbose_name = 'Rol de Pago'
        verbose_name_plural = 'Roles de Pago'

    # def calcular_remuneracion(self, sueldo_base):
    #     self.sueldo_base = (sueldo_base * self.dias_trabajados)/30

    def __str__(self):
        return u'{0}'.format(self.persona)


class Ingreso(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=255, unique=True, null=False)
    descripcion = models.TextField(verbose_name="Descripción")
    activo = models.BooleanField(verbose_name="Activo", default=True, help_text="Si se encuentra vigente")
    imprimir = models.BooleanField(verbose_name="Imprimir", default=False, help_text="Si se imprime en el Rol")
    #Se podria incluir si es fijo o no

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return u'{0}'.format(self.nombre)


class Descuento(models.Model):
    nombre = models.CharField(verbose_name="Nombre", max_length=255, unique=True, null=False)
    descripcion = models.TextField(verbose_name="Descripción")
    activo = models.BooleanField(verbose_name="Activo", default=True, help_text="Si el descuento se encuentra vigente")
    fijo = models.BooleanField(verbose_name="Fijo", default=False, help_text="Si es fijo para todos los meses")
    tipo = models.CharField(verbose_name="Tipo Descuento", max_length=100, help_text="Información Histórica",
                            choices=TIPO_DESCUENTO)  # pago quincenal o mensual (para historial)
    imprimir = models.BooleanField(verbose_name="Imprimir", default=False, help_text="Si se imprime en el Rol")

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return u'{0}'.format(self.nombre)


class Ingreso_Rol(models.Model):
    rol_pago = models.ForeignKey(Rol_Pago, on_delete=models.PROTECT, verbose_name="Rol de Pago")
    ingreso = models.ForeignKey(Ingreso, on_delete=models.PROTECT, verbose_name="Ingreso")
    valor = models.DecimalField(verbose_name="Valor ingreso", max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['pk']


class Descuento_Rol(models.Model):
    rol_pago = models.ForeignKey(Rol_Pago, on_delete=models.PROTECT, verbose_name="Rol de Pago", blank=True, null=True)
    descuento = models.ForeignKey(Descuento, on_delete=models.PROTECT, verbose_name="Descuento", blank=True, null=True)
    valor = models.DecimalField(verbose_name='Valor Descuento', max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        ordering = ['pk']


# class Presupuestacion_Partidas(models.Model):
#     numero = models.CharField(verbose_name="Número", max_length=255)
#     nombre = models.CharField(verbose_name="Nombre", max_length=255)
#     activa = models.BooleanField(verbose_name="Cuenta Activa", default=False)
#     # tipo = models.CharField(verbose_name="Tipo", choices=TIPO_CUENTAS, max_length=255)
#     orden = models.IntegerField(verbose_name="Orden", blank=True, null=True)
#     imprimir = models.BooleanField(verbose_name="Imprimir", default=True)
#
#     class Meta:
#         ordering = ['-pk']
#
#     def __str__(self):
#         return u'{0}'.format(self.nombre)


