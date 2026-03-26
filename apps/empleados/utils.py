"""
Funciones utilitarias para la aplicación de empleados
"""
import os
import uuid
from django.utils.text import slugify


def generar_nombre_foto_empleado(instance, filename):
    """
    Genera un nombre único para la foto del empleado.
    
    Formato: empleados/fotos/{empleado_id}-{uuid}.{extension}
    
    Ejemplo: empleados/fotos/1-a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6.jpg
    
    Args:
        instance: Instancia del modelo Empleado
        filename: Nombre original del archivo subido
    
    Returns:
        str: Ruta del archivo con nombre único
    """
    # Obtener extensión del archivo
    ext = os.path.splitext(filename)[1].lower()
    
    # Generar UUID único
    nombre_unico = uuid.uuid4().hex
    
    # Crear nombre con formato: empleado_id-uuid.extension
    # Ejemplo: 1-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6.jpg
    nombre_archivo = f"{instance.id}-{nombre_unico}{ext}"
    
    # Retornar ruta completa
    return f"empleados/fotos/{nombre_archivo}"


def generar_nombre_foto_con_timestamp(instance, filename):
    """
    Genera un nombre único usando timestamp.
    
    Formato: empleados/fotos/{empleado_id}-{timestamp}.{extension}
    
    Ejemplo: empleados/fotos/1-20250326101530.jpg
    
    Args:
        instance: Instancia del modelo Empleado
        filename: Nombre original del archivo subido
    
    Returns:
        str: Ruta del archivo con nombre único
    """
    from datetime import datetime
    
    # Obtener extensión del archivo
    ext = os.path.splitext(filename)[1].lower()
    
    # Obtener timestamp actual
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Crear nombre
    nombre_archivo = f"{instance.id}-{timestamp}{ext}"
    
    # Retornar ruta completa
    return f"empleados/fotos/{nombre_archivo}"


def generar_nombre_foto_descriptivo(instance, filename):
    """
    Genera un nombre descriptivo incluyendo el nombre del empleado.
    
    Formato: empleados/fotos/{empleado_id}-{slug_nombre}-{uuid_corto}.{extension}
    
    Ejemplo: empleados/fotos/1-juan-perez-a1b2c3d4.jpg
    
    Args:
        instance: Instancia del modelo Empleado
        filename: Nombre original del archivo subido
    
    Returns:
        str: Ruta del archivo con nombre descriptivo único
    """
    # Obtener extensión del archivo
    ext = os.path.splitext(filename)[1].lower()
    
    # Slug del nombre del empleado
    nombre_slug = slugify(instance.nombre)
    
    # UUID corto (primeros 8 caracteres)
    uuid_corto = uuid.uuid4().hex[:8]
    
    # Crear nombre descriptivo
    nombre_archivo = f"{instance.id}-{nombre_slug}-{uuid_corto}{ext}"
    
    # Retornar ruta completa
    return f"empleados/fotos/{nombre_archivo}"
