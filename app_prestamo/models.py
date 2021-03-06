from django.db import models
tipoEmpleado=(
    ('empleado','Empleado Planta'),
    ('contratado','Empleado Contratado'),
    ('trabajador','Trabajor'),
    ('concejal','Concejal'),)

# Create your models here
class Persona(models.Model):
    cedula = models.CharField(max_length=10, verbose_name="CÉDULA")
    nombres = models.CharField(max_length=200, verbose_name="NOMBRES")
    apellidos = models.CharField(max_length=200, verbose_name="APELLIDOS")
    telefono = models.CharField(max_length=15, verbose_name="TELÉFONO")
    tipo = models.CharField(choices=tipoEmpleado, max_length=25)
    sueldo = models.DecimalField(verbose_name="SUELDO MENSUAL", decimal_places=2, max_digits=10)

    class Meta:
        ordering = ['apellidos']

    def __str__(self):
        return "{0} {1}".format(self.nombres, self.apellidos)


class Valor_Rol(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="NOMBRE", unique=True, null=False)
    valor = models.DecimalField(verbose_name="VALOR", decimal_places=2, max_digits=10, null=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return "{0} {1}".format(self.nombre, self.valor)

class Person(models.Model):
    cedula = models.CharField(max_length=10, verbose_name="CÉDULA")
    nombres = models.CharField(max_length=200, verbose_name="NOMBRES")
    apellidos = models.CharField(max_length=200, verbose_name="APELLIDOS")
    telefono = models.CharField(max_length=15, verbose_name="TELÉFONO")
    tipo = models.CharField(choices=tipoEmpleado, max_length=25)
    sueldo = models.DecimalField(verbose_name="SUELDO MENSUAL", decimal_places=2, max_digits=10)
