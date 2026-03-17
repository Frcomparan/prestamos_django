from django.shortcuts import get_object_or_404, redirect, render

from .models import Empleado


def empleado_list(request):
	empleados = Empleado.objects.all().order_by("nombre")
	return render(request, "empleados/empleado_list.html", {"empleados": empleados})


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
