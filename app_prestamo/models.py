from django.db import models
tipoEmpleado=(
    ('empleado','Empleado'),
    ('trabajador','Trabajor'))

# Create your models here.ppi
class Persona(models.Model):
    cedula = models.CharField(max_length=10, verbose_name="CÉDULA")
    nombres = models.CharField(max_length=200, verbose_name="NOMBRES")
    apellidos = models.CharField(max_length=200, verbose_name="APELLIDOS")
    telefono = models.CharField(max_length=15, verbose_name="TELÉFONO")
    tipo = models.CharField(choices=tipoEmpleado, max_length=25)
    sueldo = models.DecimalField(verbose_name="SUELDO MENSUAL", decimal_places=2, max_digits=5)

    def __str__(self):
        return "{0} {1}".format(self.nombres, self.apellidos)