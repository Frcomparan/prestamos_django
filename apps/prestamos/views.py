from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from datetime import datetime, timedelta

from apps.empleados.models import Empleado
from .models import Prestamo

def prestamo_detail(request, pk):
	"""Detalle de un préstamo con información del empleado"""
	prestamo = get_object_or_404(Prestamo, pk=pk)
	empleado = prestamo.empleado
	puesto_actual = empleado.obtener_puesto_actual()
	
	context = {
		"prestamo": prestamo,
		"empleado": empleado,
		"puesto_actual": puesto_actual,
	}
	return render(request, "prestamos/prestamo_detail.html", context)


def prestamo_list(request):
	"""Lista préstamos con paginación y filtro por estado"""
	prestamos = Prestamo.objects.select_related("empleado").all().order_by("-fecha_solicitud", "-id")
	
	# ========== FILTRO POR ESTADO ==========
	estado_filter = request.GET.get("estado", "")
	if estado_filter:
		prestamos = prestamos.filter(estado=estado_filter)
	
	# ========== PAGINACIÓN ==========
	items_por_pagina = 10
	paginator = Paginator(prestamos, items_por_pagina)
	numero_pagina = request.GET.get("page", 1)
	
	try:
		page_obj = paginator.page(numero_pagina)
	except:
		page_obj = paginator.page(1)
	
	# ========== CONTEXTO ==========
	# Estados disponibles para el filtro
	estados = Prestamo.ESTADO_CHOICES
	
	# Parámetro de querystring para mantener filtro al paginar
	query_params = ""
	if estado_filter:
		query_params += f"&estado={estado_filter}"
	
	context = {
		"page_obj": page_obj,
		"prestamos": page_obj.object_list,
		"paginator": paginator,
		"estados": estados,
		"estado_filter": estado_filter,
		"query_params": query_params,
	}
	return render(request, "prestamos/prestamo_list.html", context)


def prestamo_create(request):
	empleados = Empleado.objects.filter(activo=True).order_by("nombre")
	context = {"empleados": empleados}

	if request.method == "POST":
		prestamo = Prestamo(
			empleado_id=request.POST.get("empleado"),
			monto=request.POST.get("monto"),
			plazo_meses=request.POST.get("plazo_meses"),
			tasa_interes_mensual=request.POST.get("tasa_interes_mensual") or 1.00,
			estado=request.POST.get("estado") or "SOLICITADO",
		)

		try:
			prestamo.full_clean()
			prestamo.save()
			return redirect("prestamo_list")
		except ValidationError as exc:
			context["errors"] = exc.messages
			context["prestamo"] = prestamo

	return render(request, "prestamos/prestamo_form.html", context)


def prestamo_update(request, pk):
	prestamo = get_object_or_404(Prestamo, pk=pk)
	empleados = Empleado.objects.filter(activo=True).order_by("nombre")
	context = {"prestamo": prestamo, "empleados": empleados}

	print(f"DEBUG: Editando préstamo {prestamo.pk} - Estado actual: {prestamo.estado}")
	print(f"Pago a capital actual: {prestamo.pago_fijo_capital}, Saldo actual: {prestamo.saldo_actual}")

	if request.method == "POST":
		prestamo.empleado_id = request.POST.get("empleado")
		prestamo.monto = request.POST.get("monto")
		prestamo.plazo_meses = request.POST.get("plazo_meses")
		prestamo.tasa_interes_mensual = request.POST.get("tasa_interes_mensual") or prestamo.tasa_interes_mensual
		prestamo.estado = request.POST.get("estado") or prestamo.estado

		try:
			prestamo.full_clean()
			prestamo.save()
			return redirect("prestamo_list")
		except ValidationError as exc:
			context["errors"] = exc.messages

	return render(request, "prestamos/prestamo_form.html", context)


def prestamo_delete(request, pk):
	prestamo = get_object_or_404(Prestamo, pk=pk)

	if request.method == "POST":
		prestamo.delete()
		return redirect("prestamo_list")

	return render(request, "prestamos/prestamo_confirm_delete.html", {"prestamo": prestamo})


# ========== ACCIONES RÁPIDAS ==========

def prestamo_aprobar(request, pk):
	"""Cambiar estado de SOLICITADO a APROBADO y establecer fecha de aprobación"""
	prestamo = get_object_or_404(Prestamo, pk=pk)
	
	if prestamo.estado == "SOLICITADO":
		prestamo.estado = "APROBADO"
		prestamo.fecha_aprobacion = datetime.now().date()
		prestamo.save()
	
	return redirect("prestamo_list")


def prestamo_rechazar(request, pk):
	"""Cambiar estado de SOLICITADO a RECHAZADO"""
	prestamo = get_object_or_404(Prestamo, pk=pk)
	
	if prestamo.estado == "SOLICITADO":
		prestamo.estado = "RECHAZADO"
		prestamo.save()
	
	return redirect("prestamo_list")


def prestamo_liberar(request, pk):
	"""Cambiar estado de APROBADO a ACTIVO y establecer fechas de descuento"""
	prestamo = get_object_or_404(Prestamo, pk=pk)
	
	if prestamo.estado == "APROBADO":
		hoy = datetime.now().date()
		
		# Fecha de inicio de descuento: un mes después de la liberación
		prestamo.fecha_inicio_descuento = hoy + timedelta(days=30)
		
		# Fecha de fin de descuento: hoy + plazo_meses
		prestamo.fecha_fin_descuento = hoy + timedelta(days=30 * prestamo.plazo_meses)
		
		prestamo.estado = "ACTIVO"
		prestamo.save()
	
	return redirect("prestamo_list")
