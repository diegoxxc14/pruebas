from django.shortcuts import render, redirect
from django.http import HttpResponse
from app_libros.forms import BookForm, PeriodoForm
from django.shortcuts import get_list_or_404, get_object_or_404
from app_libros.models import Persona, Rol_Pago, Descuento, Descuento_Rol, Periodo_Rol
from decimal import Decimal

# Create your views here.
def inicio(request):
    #return HttpResponse("Hola mundo")
    return render(request, 'libros/index.html')

def libro_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('book:inicio')
    else:
        form = BookForm()

    return render(request, 'libros/libros_form.html',{'form':form})
#
# def calcularIees_view(rolPago, valor_empleado = Decimal(11.45), valor_trabajador = Decimal(9.45)):
#     pk_descuento = get_object_or_404(Descuento, nombre='IEES').pk
#     descuento_iees = rolPago.persona.sueldo
#     if rolPago.persona.tipo == 'trabajador':
#         descuento_iees = (descuento_iees * valor_trabajador)/100
#     elif rolPago.persona.tipo == 'empleado':
#         descuento_iees = (descuento_iees * valor_empleado)/100
#     dr = Descuento_Rol(
#         rolPago_id=rolPago.pk,
#         descuento_id=pk_descuento,
#         valor=descuento_iees
#     )
#     dr.save()
#
def generar_roles_view(empleados,pk_periodo):
    for emp in empleados:
        rp = Rol_Pago(
            codigo = u'Rol de Pago - {0}'.format(emp),
            persona_id = emp.pk,
            periodo_rol_id = pk_periodo)
        rp.save()
        #calcularIees_view(rp)
    return get_list_or_404(Rol_Pago, periodo_rol=pk_periodo)
#
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
#
# def periodo_detalle_view(request):
#     p = get_list_or_404(Periodo_Rol)
#     return render(request, 'libros/periodo_ver.html',{'periodos':p})
#
# def rol_detalle_view(request, pk):
#     r = get_list_or_404(Rol_Pago, periodo_rol_id=pk)
#     return render(request, 'libros/roles_generar.html', {'periodo':get_object_or_404(Periodo_Rol,pk=pk),'roles':r})
#
# def descuento_view(request, pk):
#     d = get_list_or_404(Descuento_Rol, rolPago_id=pk)
#     return render(request, 'libros/descuentos_ver.html',{'descuentos':d})