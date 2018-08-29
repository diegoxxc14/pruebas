from django.shortcuts import render, redirect
from app_libros.forms import PeriodoForm
from django.shortcuts import get_list_or_404, get_object_or_404
from app_libros.models import Persona, Rol_Pago, Descuento, Descuento_Rol, Periodo_Rol, Ingreso, Ingreso_Rol
from decimal import Decimal
from django.contrib.auth.decorators import login_required

# Create your views here.
from app_prestamo.models import Valor_Rol


def inicio(request):
    #return HttpResponse("Hola mundo")
    return render(request, 'libros/index.html')

def cal_iess_personal(rolPago, valor_empleado, valor_trabajador):
    ing_rol = get_object_or_404(Ingreso_Rol, rol_pago=rolPago.pk, ingreso=1)

    if rolPago.persona.tipo == 'trabajador':
        return (ing_rol.valor * valor_trabajador)/100
    else:
        return (ing_rol.valor * valor_empleado)/100


def cal_iess_patronal(rolPago, valor):
    ing_rol = get_object_or_404(Ingreso_Rol, rol_pago=rolPago.pk, ingreso=1)
    return (ing_rol.valor * valor)/100


def generar_ingresos(rolPago):
    ingresos = get_list_or_404(Ingreso, activo=True)

    for ingreso in ingresos:
        ir = Ingreso_Rol(
            rol_pago_id=rolPago.pk,
            ingreso_id=ingreso.pk,
        )
        if ingreso.pk == 1 and rolPago.dias_trabajados != 0: # Id 1 para el suedo (OJO)
            ir.valor = rolPago.persona.sueldo   #Al generar por 1ra vez agregamos el sueldo base
        ir.save()


def generar_descuentos(rolPago, iess_per_empleado, iess_per_trabajador):
    descuentos = get_list_or_404(Descuento, activo=True)

    for descuento in descuentos:
        dr = Descuento_Rol(
            rol_pago_id=rolPago.pk,
            descuento_id=descuento.pk,
        )
        if descuento.pk == 1 and rolPago.dias_trabajados != 0:# Id 1 para el iess (OJO)
            dr.valor = cal_iess_personal(rolPago, iess_per_empleado, iess_per_trabajador)
        dr.save()


def generar_roles(empleados, pk_periodo):
    valores_rol = get_list_or_404(Valor_Rol)
    SUELDO_BASICO = valores_rol[0].valor
    FONDO_RESERVA = valores_rol[1].valor
    IESS_PER_EMP = valores_rol[2].valor
    IESS_PER_TRA = valores_rol[3].valor
    IESS_PATRONAL = valores_rol[4].valor

    for emp in empleados:
        rp = Rol_Pago(
            persona_id = emp.pk,
            periodo_rol_id = pk_periodo,
        )
        if emp.tipo == 'contratado':
            rp.dias_trabajados = 0  #Por defecto son 30 para trabajadores y empleados planta
        rp.save()

        generar_ingresos(rp)   # cargamos los ingresos activos al Rol
        generar_descuentos(rp, Decimal(valores_rol[2].valor), Decimal(valores_rol[3].valor)) #generamos los descuentos al Rol

        if emp.tipo != 'contratado':    #El Rol del contratado se genera en 0
            cal_rol_pago(rp, Decimal(valores_rol[4].valor))

    return get_list_or_404(Rol_Pago, periodo_rol=pk_periodo)


@login_required()
def crear_periodo_view(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            periodo_new = form.save()
            personas = get_list_or_404(Persona)#Lista de partidas para los roles
            roles = generar_roles(personas, periodo_new.pk)
            return render(request, 'libros/roles_generar.html', {'periodo':periodo_new,'roles':roles})
    else:
        form = PeriodoForm()
    return render(request, 'libros/periodo_form.html',{'form': form})


def ver_periodos_view(request):
    p = get_list_or_404(Periodo_Rol)
    return render(request, 'libros/periodo_ver.html',{'periodos':p})


def ver_roles_view(request, pk):
    r = get_list_or_404(Rol_Pago, periodo_rol_id=pk)
    p = get_object_or_404(Periodo_Rol, pk=pk)
    return render(request, 'libros/roles_generar.html', {'periodo':p,'roles':r})


def ver_detalle_rol_view(request, pk):
    rolPago = get_object_or_404(Rol_Pago, pk=pk)
    des = get_list_or_404(Descuento_Rol, rol_pago_id=pk)
    ing = get_list_or_404(Ingreso_Rol, rol_pago_id=pk)
    return render(request, 'libros/detalle_rol.html', {'descuentos':des, 'ingresos':ing, 'rol':rolPago})

def cal_rol_pago(rolPago, valor_iess_patronal):
    ingresos_rol = get_list_or_404(Ingreso_Rol, rol_pago=rolPago.pk)
    descuentos_rol = get_list_or_404(Descuento_Rol, rol_pago=rolPago.pk)
    iess_patronal = cal_iess_patronal(rolPago, valor_iess_patronal)

    sum_ingresos = cal_total(ingresos_rol)
    sum_descuentos = cal_total(descuentos_rol)
    total_rol = sum_ingresos - sum_descuentos

    rolPago.aporte_patronal = iess_patronal
    rolPago.total_ingresos = sum_ingresos
    rolPago.total_descuentos = sum_descuentos
    rolPago.total_pagar = total_rol
    rolPago.save()

def cal_total(valores_rol):    #Calcula el total de ingresos y egresos
    sum_total = Decimal(0.0)
    for valor_rol in valores_rol:
        sum_total+=valor_rol.valor
    return sum_total

# def ver_personas(request, template_name='libros/DataTable.html'):
#     personas = get_list_or_404(Persona)
#     return render(request, template_name,{'personas':personas})


from django.views.generic import ListView, TemplateView
from app_prestamo.models import *
from django.core import serializers
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

class listar_rolesPago(ListView):
    model = Person
    template_name = 'libros/DataTable.html'
    context_object_name = 'personas'

def cargar_rolesPago_ajax(request):
    list_personas = get_list_or_404(Person)
    data = serializers.serialize('json',list_personas)
    return HttpResponse(data, content_type='application/json')

class delete_persona_ajax(TemplateView):

    def get(self, request, *args, **kwargs):
        id_per = request.GET['id']
        if int(id_per) != 0:
            per_remove = Person.objects.get(pk=id_per)
            per_remove.delete()
        list_personas = get_list_or_404(Person)
        data = serializers.serialize('json',list_personas)
        return HttpResponse(data, content_type='application/json')


@csrf_exempt #Directiva para que el {% csrf_token %} funcione con POST
def remover_rolesPago_ajax(request):

    if request.POST:
        ids_per = json.loads(request.POST['pks'])#cargo el valor de POST como una lista
        personas_remove = Person.objects.filter(pk__in=ids_per)
        personas_remove.delete()
        return HttpResponse(request)


@csrf_exempt #Directiva para que el {% csrf_token %} funcione con POST
def crear_rolPago_ajax(request):

    if request.POST:
        rol_pago = json.loads(request.POST['rol_pago'])  # cargo el valor de POST como una lista
        persona_new = Person(cedula=rol_pago[0],sueldo=Decimal(rol_pago[1]), nombres=rol_pago[2], apellidos=rol_pago[3])
        persona_new.save()
        data = serializers.serialize('json',get_list_or_404(Person, pk=persona_new.id))
        return HttpResponse(data, content_type='application/json')