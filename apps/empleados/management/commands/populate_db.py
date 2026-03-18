from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.empleados.models import Puesto, Empleado, HistorialPuesto
from apps.prestamos.models import Prestamo


class Command(BaseCommand):
    """
    Comando para poblar la base de datos con datos de ejemplo.
    
    Uso:
        python manage.py populate_db
        python manage.py populate_db --clear
    """
    
    help = 'Puebla la base de datos con datos de ejemplo para empleados y préstamos'

    def add_arguments(self, parser):
        """Define argumentos opcionales para el comando"""
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los datos existentes antes de poblar la BD',
        )

    def handle(self, *args, **options):
        """Método principal que ejecuta el comando"""
        
        # Opción de limpiar datos
        if options['clear']:
            self._clear_data()
        
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("INICIANDO POBLACIÓN DE DATOS"))
        self.stdout.write(self.style.SUCCESS("=" * 60))
        
        # Ejecutar las funciones de población
        self._create_puestos()
        self._create_empleados()
        self._create_prestamos()
        
        self.stdout.write(self.style.SUCCESS("=" * 60))
        self.stdout.write(self.style.SUCCESS("✓ POBLACIÓN DE DATOS COMPLETADA EXITOSAMENTE"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

    def _clear_data(self):
        """Elimina todos los datos de las tablas"""
        self.stdout.write(self.style.WARNING("Eliminando datos existentes..."))
        Prestamo.objects.all().delete()
        HistorialPuesto.objects.all().delete()
        Empleado.objects.all().delete()
        Puesto.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Datos eliminados"))

    def _create_puestos(self):
        """Crea los puestos de trabajo"""
        self.stdout.write("\n📋 CREANDO PUESTOS DE TRABAJO...")
        
        puestos_data = [
            {'nombre': 'Gerente General', 'sueldo': Decimal('5000.00')},
            {'nombre': 'Desarrollador Senior', 'sueldo': Decimal('4000.00')},
            {'nombre': 'Desarrollador Junior', 'sueldo': Decimal('2500.00')},
            {'nombre': 'Analista de Sistemas', 'sueldo': Decimal('3500.00')},
            {'nombre': 'Administrativo', 'sueldo': Decimal('2000.00')},
        ]
        
        self.puestos = {}
        for data in puestos_data:
            puesto, created = Puesto.objects.get_or_create(
                nombre=data['nombre'],
                defaults={'sueldo': data['sueldo']}
            )
            self.puestos[data['nombre']] = puesto
            
            if created:
                self.stdout.write(
                    f"  {puesto.nombre:<30} - ${puesto.sueldo}"
                )
            else:
                self.stdout.write(
                    f"  {puesto.nombre} (ya existe)"
                )

    def _create_empleados(self):
        """Crea 30+ empleados con historiales de puestos"""
        self.stdout.write("\n👥 CREANDO EMPLEADOS (30+ empleados)...")
        
        today = timezone.now().date()
        
        # Lista de 30+ empleados con antigüedad variable
        empleados_data = [
            # Empleados con antigüedad de 2+ años (elegibles para préstamos múltiples)
            {'nombre': 'Juan Pérez González', 'puesto': 'Gerente General', 'dias_antiguedad': 730, 'activo': True},
            {'nombre': 'María García López', 'puesto': 'Desarrollador Senior', 'dias_antiguedad': 550, 'activo': True},
            {'nombre': 'Carlos López Martínez', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 365, 'activo': True},
            {'nombre': 'Ana Martínez Rodríguez', 'puesto': 'Analista de Sistemas', 'dias_antiguedad': 550, 'activo': True},
            {'nombre': 'Roberto Sánchez Gómez', 'puesto': 'Administrativo', 'dias_antiguedad': 450, 'activo': True},
            {'nombre': 'Daniela Flores Moreno', 'puesto': 'Desarrollador Senior', 'dias_antiguedad': 700, 'activo': True},
            {'nombre': 'Fernando Rodríguez Cruz', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 380, 'activo': True},
            {'nombre': 'Patricia Gómez Sosa', 'puesto': 'Analista de Sistemas', 'dias_antiguedad': 600, 'activo': True},
            {'nombre': 'Miguel Ángel Torres Ruiz', 'puesto': 'Desarrollador Senior', 'dias_antiguedad': 850, 'activo': True},
            {'nombre': 'Victoria López Peña', 'puesto': 'Administrativo', 'dias_antiguedad': 500, 'activo': True},
            
            # Empleados con antigüedad moderada (1-1.5 años)
            {'nombre': 'Javier Castillo Vargas', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 420, 'activo': True},
            {'nombre': 'Sofía Ramírez Flores', 'puesto': 'Analista de Sistemas', 'dias_antiguedad': 450, 'activo': True},
            {'nombre': 'Gonzalo Diaz Hernández', 'puesto': 'Administrativo', 'dias_antiguedad': 380, 'activo': True},
            {'nombre': 'Mariana Cortés Gutiérrez', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 395, 'activo': True},
            {'nombre': 'Andrés Moreno Silva', 'puesto': 'Desarrollador Senior', 'dias_antiguedad': 480, 'activo': True},
            
            # Empleados nuevos (< 1 año, sin acceso a préstamos)
            {'nombre': 'Claudia Mendoza Ortiz', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 280, 'activo': True},
            {'nombre': 'David Herrera Salazar', 'puesto': 'Administrativo', 'dias_antiguedad': 150, 'activo': True},
            {'nombre': 'Elena Rojas Vargas', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 220, 'activo': True},
            {'nombre': 'Felipe Soto Muñoz', 'puesto': 'Analista de Sistemas', 'dias_antiguedad': 90, 'activo': True},
            {'nombre': 'Graciela Navarro Campos', 'puesto': 'Administrativo', 'dias_antiguedad': 180, 'activo': True},
            
            # Empleados con antigüedad moderada-alta (más candidatos para múltiples préstamos)
            {'nombre': 'Hugo Mendez Reyes', 'puesto': 'Desarrollador Senior', 'dias_antiguedad': 520, 'activo': True},
            {'nombre': 'Iris Campos López', 'puesto': 'Administrativo', 'dias_antiguedad': 620, 'activo': True},
            {'nombre': 'Julio Fernández Blanco', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 400, 'activo': True},
            {'nombre': 'Karina Rivas Montoya', 'puesto': 'Analista de Sistemas', 'dias_antiguedad': 560, 'activo': True},
            {'nombre': 'Luis Alberto García Díaz', 'puesto': 'Gerente General', 'dias_antiguedad': 900, 'activo': True},
            
            # Más empleados para tener 25+
            {'nombre': 'Marcela Jimenez Vargas', 'puesto': 'Desarrollador Senior', 'dias_antiguedad': 580, 'activo': True},
            {'nombre': 'Nicolás Peña Cordova', 'puesto': 'Administrativo', 'dias_antiguedad': 470, 'activo': True},
            {'nombre': 'Olivia Rodriga Silva', 'puesto': 'Analista de Sistemas', 'dias_antiguedad': 410, 'activo': True},
            {'nombre': 'Pablo Morales Gómez', 'puesto': 'Desarrollador Junior', 'dias_antiguedad': 320, 'activo': True},
            {'nombre': 'Quinton Vega López', 'puesto': 'Administrativo', 'dias_antiguedad': 240, 'activo': True},
        ]

        self.empleados = {}
        self.empleados_con_prestamos = []  # Guardar empleados elegibles para préstamos
        
        count_creados = 0
        for data in empleados_data:
            fecha_ingreso = today - timedelta(days=data['dias_antiguedad'])
            
            empleado, created = Empleado.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    'fecha_ingreso': fecha_ingreso,
                    'activo': data['activo'],
                }
            )
            self.empleados[data['nombre']] = empleado
            
            if created:
                count_creados += 1
                self.stdout.write(
                    f"  ✓ {empleado.nombre:<35} (Desde: {fecha_ingreso})"
                )
                
                # Asignar puesto actual
                puesto = self.puestos[data['puesto']]
                HistorialPuesto.objects.create(
                    empleado=empleado,
                    puesto=puesto,
                    fecha_inicio=fecha_ingreso,
                    fecha_fin=None  # Puesto actual (sin fecha de fin)
                )
                self.stdout.write(
                    f"      └─ Puesto: {puesto.nombre} (${puesto.sueldo})"
                )
                
                # Guardar empleados con antigua antigüedad para asignarles préstamos
                if data['dias_antiguedad'] >= 365:  # 1+ año
                    self.empleados_con_prestamos.append(empleado)
            else:
                self.stdout.write(
                    f"  ⚠ {empleado.nombre} (ya existe)"
                )
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Total de empleados creados: {count_creados}"))

    def _create_prestamos(self):
        """Crea múltiples préstamos para empleados elegibles (15+ empleados con 1-6 préstamos)"""
        self.stdout.write("\n💰 CREANDO PRÉSTAMOS (respetando lógica de negocio)...")
        
        today = timezone.now().date()
        
        # Seleccionar 15 empleados con antigüedad >= 1 año para asignarles préstamos
        empleados_prestatarios = self.empleados_con_prestamos[:15]
        
        self.stdout.write(f"   Asignando préstamos a {len(empleados_prestatarios)} empleados...\n")
        
        prestamos_totales = 0
        
        for idx, empleado in enumerate(empleados_prestatarios, 1):
            # Determinar cuántos préstamos tendrá este empleado (1-6)
            # Los primeros empleados tienen más préstamos para variar
            if idx <= 5:
                num_prestamos = 4 + (idx % 3)  # 4-6 préstamos
            elif idx <= 10:
                num_prestamos = 2 + (idx % 3)  # 2-4 préstamos
            else:
                num_prestamos = 1 + (idx % 3)  # 1-3 préstamos
            
            self.stdout.write(
                f"  └─ {empleado.nombre:<35} → {num_prestamos} préstamo(s)"
            )
            
            # Estados posibles para los préstamos
            # Solo 1 puede ser ACTIVO
            estados = ['SOLICITADO', 'APROBADO', 'CONCLUIDO', 'RECHAZADO']
            estado_activo_usado = False
            
            for i in range(num_prestamos):
                # Definir estado del préstamo
                if i == 0 and not estado_activo_usado:
                    # El primer préstamo tiene chances de ser ACTIVO
                    if idx % 2 == 0:  # 50% de chance
                        estado = 'ACTIVO'
                        estado_activo_usado = True
                    else:
                        estado = 'APROBADO'
                else:
                    # Otros préstamos: variar estados (pero no ACTIVO)
                    estado = estados[i % len(estados)]
                
                # Generar datos del préstamo con variación
                monto = Decimal(str(1000 + (i * 500) + (idx * 100)))  # Montos variados
                plazo_meses = 3 + (i * 2)  # 3, 5, 7, 9, 11, 13 meses
                tasa_interes = Decimal('1.00')
                
                # Fecha de solicitud: variar entre hace 120 días y hace 10 días
                dias_solicitud = 120 - (i * 15) - (idx * 2)
                fecha_solicitud = today - timedelta(days=abs(dias_solicitud))
                
                # Crear préstamo con get_or_create
                prestamo, created = Prestamo.objects.get_or_create(
                    empleado=empleado,
                    monto=monto,
                    plazo_meses=plazo_meses,
                    defaults={
                        'tasa_interes_mensual': tasa_interes,
                        'estado': estado,
                        'fecha_solicitud': fecha_solicitud,
                    }
                )
                
                if created:
                    prestamos_totales += 1
                    estado_display = f"[{estado}]"
                    self.stdout.write(
                        f"      ✓ Préstamo #{i+1}: ${monto} en {plazo_meses}m {estado_display}"
                    )
                else:
                    self.stdout.write(
                        f"      ⚠ Préstamo #{i+1} ya existe"
                    )
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Total de préstamos creados: {prestamos_totales}"))
        self.stdout.write(self.style.WARNING(
            f"   (Respeto:** máximo 1 ACTIVO por empleado)"
        ))
