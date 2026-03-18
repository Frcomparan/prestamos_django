from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
# from django.db.models import Q

from .models import Empleado, Puesto


def empleado_list(request):
	"""Lista empleados con paginación y filtros (activo, puesto actual)"""
	empleados = Empleado.objects.all().order_by("nombre")
	
	# ========== FILTROS ==========
	# Filtro por activo
	activo_filter = request.GET.get("activo", "")
	if activo_filter == "si":
		empleados = empleados.filter(activo=True)
	elif activo_filter == "no":
		empleados = empleados.filter(activo=False)
	
	# Filtro por puesto actual
	puesto_filter = request.GET.get("puesto", "")
	if puesto_filter:
		empleados = empleados.filter(
			historial_puestos__puesto_id=puesto_filter,
			historial_puestos__fecha_fin__isnull=True
		).distinct()
	
	# ========== PAGINACIÓN ==========
	items_por_pagina = 10
	paginator = Paginator(empleados, items_por_pagina)
	numero_pagina = request.GET.get("page", 1)
	
	try:
		page_obj = paginator.page(numero_pagina)
	except:
		page_obj = paginator.page(1)
	
	# ========== CONTEXTO ==========
	# Obtener puestos disponibles para el filtro
	puestos = Puesto.objects.all().order_by("nombre")
	
	# Parámetros de querystring para mantener filtros al paginar
	query_params = ""
	if activo_filter:
		query_params += f"&activo={activo_filter}"
	if puesto_filter:
		query_params += f"&puesto={puesto_filter}"
	
	context = {
		"page_obj": page_obj,
		"empleados": page_obj.object_list,
		"paginator": paginator,
		"puestos": puestos,
		"activo_filter": activo_filter,
		"puesto_filter": puesto_filter,
		"query_params": query_params,
	}
	return render(request, "empleados/empleado_list.html", context)


def empleado_detail(request, pk):
	empleado = get_object_or_404(Empleado, pk=pk)
	historial = empleado.historial_puestos.all().order_by("-fecha_inicio")
	prestamos = empleado.prestamos.all().order_by("-fecha_solicitud")
	
	context = {
		"empleado": empleado,
		"historial": historial,
		"prestamos": prestamos,
	}
	return render(request, "empleados/empleado_detail.html", context)


def empleado_create(request):
	if request.method == "POST":
		nombre = request.POST.get("nombre", "").strip()
		fecha_ingreso = request.POST.get("fecha_ingreso")
		activo = request.POST.get("activo", "").lower() in {"on", "true", "1", "si"}

		Empleado.objects.create(
			nombre=nombre,
			fecha_ingreso=fecha_ingreso,
			activo=activo,
		)
		return redirect("empleado_list")

	return render(request, "empleados/empleado_form.html")


def empleado_update(request, pk):
	empleado = get_object_or_404(Empleado, pk=pk)

	if request.method == "POST":
		empleado.nombre = request.POST.get("nombre", "").strip()
		empleado.fecha_ingreso = request.POST.get("fecha_ingreso")
		empleado.activo = request.POST.get("activo", "").lower() in {"on", "true", "1", "si"}
		empleado.save()
		return redirect("empleado_list")

	return render(request, "empleados/empleado_form.html", {"empleado": empleado})


def empleado_delete(request, pk):
	empleado = get_object_or_404(Empleado, pk=pk)

	if request.method == "POST":
		empleado.delete()
		return redirect("empleado_list")

	return render(request, "empleados/empleado_confirm_delete.html", {"empleado": empleado})
