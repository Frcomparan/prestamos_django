from django.urls import path

from . import views

urlpatterns = [
    path("", views.prestamo_list, name="prestamo_list"),
    path("nuevo/", views.prestamo_create, name="prestamo_create"),
    path("<int:pk>/", views.prestamo_detail, name="prestamo_detail"),
    path("<int:pk>/editar/", views.prestamo_update, name="prestamo_update"),
    path("<int:pk>/eliminar/", views.prestamo_delete, name="prestamo_delete"),

    # Abonos
    path("<int:pk>/abonar/", views.abono_create, name="abono_create"),
    
    # Acciones rápidas
    path("<int:pk>/aprobar/", views.prestamo_aprobar, name="prestamo_aprobar"),
    path("<int:pk>/rechazar/", views.prestamo_rechazar, name="prestamo_rechazar"),
    path("<int:pk>/liberar/", views.prestamo_liberar, name="prestamo_liberar"),
]
