# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-15 03:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_prestamo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300, verbose_name='NOMBRES')),
                ('fecha_nac', models.DateField(verbose_name='FECHA NACIMIENTO')),
                ('fecha_mue', models.DateField(verbose_name='FECHA MUERTE')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, verbose_name='CÓDIGO')),
                ('titulo', models.CharField(max_length=300, verbose_name='TÍTULO')),
                ('resumen', models.CharField(max_length=500, verbose_name='RESUMEN')),
                ('imprenta', models.CharField(max_length=200, verbose_name='IMPRENTA')),
                ('nro_pag', models.IntegerField(default=0, verbose_name='NRO. PÁGINAS')),
                ('fecha_pub', models.DateField(verbose_name='FECHA PUBLICACIÓN')),
                ('autor', models.ManyToManyField(to='app_libros.Author')),
                ('persona', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_prestamo.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='Descuento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('activo', models.BooleanField(default=True, help_text='Si es activo para todos los meses', verbose_name='Activo')),
                ('fijo', models.BooleanField(default=False, help_text='Si es fijo para todos los meses', verbose_name='Fijo')),
                ('tipo', models.CharField(choices=[('mensual', 'Mensual'), ('quincenal', 'Quincenal')], help_text='Información Histórica', max_length=100, verbose_name='Tipo Descuento')),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Descuento_Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, verbose_name='Valor Descuento')),
                ('descuento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_libros.Descuento', verbose_name='Descuento')),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True, verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('activo', models.BooleanField(default=True, help_text='Si es activo para todos los meses', verbose_name='Activo')),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso_Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=9, verbose_name='Valor ingreso')),
                ('ingreso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_libros.Ingreso', verbose_name='Ingreso')),
            ],
        ),
        migrations.CreateModel(
            name='Periodo_Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(choices=[('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')], max_length=15, verbose_name='Mes')),
                ('anio', models.IntegerField(verbose_name='Año')),
                ('max_dias', models.IntegerField(default=30)),
                ('emitido', models.BooleanField(default=False, verbose_name='Completado')),
                ('fecha_emision', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Periodo',
                'verbose_name_plural': 'Periodos',
            },
        ),
        migrations.CreateModel(
            name='Presupuestacion_Partidas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=255, verbose_name='Número')),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombre')),
                ('activa', models.BooleanField(default=False, verbose_name='Cuenta Activa')),
                ('orden', models.IntegerField(blank=True, null=True, verbose_name='Orden')),
                ('imprimir', models.BooleanField(default=True, verbose_name='Imprimir')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Rol_Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Rol de Pagos')),
                ('periodo_rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_libros.Periodo_Rol', verbose_name='Periodo')),
                ('persona', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='partida_rol', to='app_prestamo.Persona', verbose_name='Partida')),
            ],
            options={
                'verbose_name': 'Rol de Pago',
                'verbose_name_plural': 'Roles de Pago',
                'ordering': ['-pk'],
            },
        ),
        migrations.AddField(
            model_name='ingreso_rol',
            name='rol_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_libros.Rol_Pago', verbose_name='Rol de Pago'),
        ),
        migrations.AddField(
            model_name='descuento_rol',
            name='rol_pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_libros.Rol_Pago', verbose_name='Rol de Pago'),
        ),
    ]
