from django.shortcuts import render, redirect
from app_libros.forms import PeriodoForm
from django.shortcuts import get_list_or_404, get_object_or_404
from app_libros.models import Persona, Rol_Pago, Descuento, Descuento_Rol, Periodo_Rol, Ingreso, Ingreso_Rol
from decimal import Decimal
from django.contrib.auth.decorators import login_required

# Create your views here.
def inicio(request):
    #return HttpResponse("Hola mundo")
    return render(request, 'libros/index.html')

def calcular_iess_view(rolPago, valor_empleado = Decimal(11.45), valor_trabajador = Decimal(9.45)):
    sueldo_base = rolPago.persona.sueldo

    if rolPago.persona.tipo == 'trabajador':
        return (sueldo_base * valor_trabajador)/100
    elif rolPago.persona.tipo == 'empleado':
        return (sueldo_base * valor_empleado)/100

def cargar_sueldo_view(rolPago):
    pk_ingreso = get_object_or_404(Ingreso, nombre='SUELDO').pk
    sueldo_base = rolPago.persona.sueldo

    ir = Ingreso_Rol(
        rol_pago_id=rolPago.pk,
        ingreso_id=pk_ingreso,
        valor=sueldo_base
    )
    ir.save()

def generar_ingresos_view(rolPago):
    ingresos = get_list_or_404(Ingreso, activo=True)

    for ingreso in ingresos:
        ir = Ingreso_Rol(
            rol_pago_id=rolPago.pk,
            ingreso_id=ingreso.pk,
        )
        if ingreso.nombre == 'SUELDO':#Cambiamos el valor de default
            ir.valor = rolPago.persona.sueldo
        ir.save()

def generar_descuentos_view(rolPago):
    descuentos = get_list_or_404(Descuento, activo=True)

    for descuento in descuentos:
        dr = Descuento_Rol(
            rol_pago_id=rolPago.pk,
            descuento_id=descuento.pk,
        )
        if descuento.nombre == 'IESS':#Cambiamos el valor de default
            dr.valor = calcular_iess_view(rolPago)
        dr.save()

def generar_roles_view(empleados,pk_periodo):
    for emp in empleados:
        rp = Rol_Pago(
            codigo = u'Rol de Pago - {0}'.format(emp),
            persona_id = emp.pk,
            periodo_rol_id = pk_periodo)
        rp.save()

        generar_ingresos_view(rp)  # cargamos los ingresos activos al Rol
        generar_descuentos_view(rp)#generamos los descuentos al Rol

    return get_list_or_404(Rol_Pago, periodo_rol=pk_periodo)

@login_required()
def crear_periodo_view(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            periodo_new = form.save()
            personas = get_list_or_404(Persona)#Lista de empleados o partidas para los roles
            roles = generar_roles_view(personas, periodo_new.pk)

            return render(request, 'libros/roles_generar.html', {'periodo':periodo_new,'roles':roles})
        # return redirect('inicio')
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
    des = get_list_or_404(Descuento_Rol, rol_pago_id=pk)
    ing = get_list_or_404(Ingreso_Rol, rol_pago_id=pk)
    return render(request, 'libros/detalle_rol.html', {'descuentos':des, 'ingresos':ing})