from rest_framework import viewsets
from parametros.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.db.models import Avg, Count, F
from rest_framework import status
from django.db.models import Max

# Create your views here.
@api_view(['GET'])
def EstudiantesCarreraAnio(request,codigo_carrera,anio_cursado):
    try:
        if codigo_carrera=='0' and anio_cursado=='0':
            estudiante = Estudiante.objects.filter(inscrito_gestion='si', anio_cursado__in=['PRIMER AÑO', 'SEGUNDO AÑO', 'TERCER AÑO', 'CUARTO AÑO', 'QUINTO AÑO']).order_by('anio_cursado')
            estudiante_serializer=EstudianteCarreraAnioSerializer(estudiante,many=True).data 
            nombre_carrera='TODOS'
            numero_estudiantes=estudiante.count()
            anio_cursado='TODOS'
            return Response({"año":anio_cursado,
                            "carrera":nombre_carrera,
                            "numero_estudiantes":numero_estudiantes,
                            "estudiantes":estudiante_serializer})
    
        if codigo_carrera!='0' and anio_cursado=='0':
            estudiante=Estudiante.objects.filter(codigo_carrera=codigo_carrera, inscrito_gestion='si',anio_cursado__in=['PRIMER AÑO', 'SEGUNDO AÑO', 'TERCER AÑO', 'CUARTO AÑO', 'QUINTO AÑO']).order_by('anio_cursado')
            estudiante_serializer=EstudianteCarreraAnioSerializer(estudiante,many=True).data       
            nombre_carrera=Carrera.objects.filter(codigo_carrera=codigo_carrera).first().nombre_carrera
            numero_estudiantes=estudiante.count()
            anio_cursado='TODOS'
            return Response({"año":anio_cursado,
                            "carrera":nombre_carrera,
                            "numero_estudiantes":numero_estudiantes,
                            "estudiantes":estudiante_serializer})
    
        if codigo_carrera!='0' and anio_cursado!='0':
            
            estudiante=Estudiante.objects.filter(codigo_carrera=codigo_carrera,anio_cursado=anio_cursado, inscrito_gestion='si').order_by('anio_cursado')            
            estudiante_serializer=EstudianteCarreraAnioSerializer(estudiante,many=True).data
            nombre_carrera=Carrera.objects.filter(codigo_carrera=codigo_carrera).first().nombre_carrera
            numero_estudiantes=estudiante.count()

            return Response({"año":anio_cursado,
                            "carrera":nombre_carrera,
                            "numero_estudiantes":numero_estudiantes,
                            "estudiantes":estudiante_serializer})
    except:
        return Response({"message":"vuelva a ingresar correctamente los valores"})
    
@api_view(['GET'])
def EstudiantesInscritosGenero(request):
    anios = ['PRIMER AÑO', 'SEGUNDO AÑO', 'TERCER AÑO', 'CUARTO AÑO', 'QUINTO AÑO']
    carreras = Carrera.objects.all()
    reporte = []

    for carrera in carreras:
        estudiantes_varones = Estudiante.objects.filter(codigo_carrera=carrera.codigo_carrera, genero='M', inscrito_gestion='si', anio_cursado__in=anios)
        numero_varones = estudiantes_varones.count()
        estudiantes_mujeres = Estudiante.objects.filter(codigo_carrera=carrera.codigo_carrera, genero='F', inscrito_gestion='si', anio_cursado__in=anios)
        numero_mujeres = estudiantes_mujeres.count()
        auxiliar = [carrera.nombre_carrera, numero_varones, numero_mujeres]
        reporte.append(auxiliar)

    # Total de estudiantes varones y mujeres en todas las carreras
    total_varones = Estudiante.objects.filter(genero='M', inscrito_gestion='si', anio_cursado__in=anios).count()
    total_mujeres = Estudiante.objects.filter(genero='F', inscrito_gestion='si', anio_cursado__in=anios).count()
    auxiliar_total = ["TOTAL VARONES Y MUJERES", total_varones, total_mujeres]
    reporte.append(auxiliar_total)

    if reporte:
        return Response(reporte)
    else:
        return Response({"message": "no se encontró ningún estudiante, ingrese datos válidos"})

@api_view(['GET'])
def EstudiantesInscritosPorDepartamentos(request):
    departamentos = ['COCHABAMBA', 'LA PAZ', 'SANTA CRUZ', 'ORURO', 'POTOSI','CHUQUISACA','TARIJA','BENI','PANDO']
    anios = ['PRIMER AÑO', 'SEGUNDO AÑO', 'TERCER AÑO', 'CUARTO AÑO', 'QUINTO AÑO']
    carreras = Carrera.objects.all()
    reporte = []

    for carrera in carreras:
        auxiliar=[carrera.nombre_carrera]
        for departamento in departamentos:
            estudiantes = Estudiante.objects.filter(codigo_carrera=carrera.codigo_carrera,depa_nacimiento=departamento, inscrito_gestion='si',anio_cursado__in=anios)
            numero = estudiantes.count()
            if numero:
                auxiliar.append(numero)
            else:
                auxiliar.append("-")
        estudiantes = Estudiante.objects.filter(codigo_carrera=carrera.codigo_carrera, inscrito_gestion='si',anio_cursado__in=anios)
        numero = estudiantes.count()
        if numero:
            auxiliar.append(numero)
        else:
            auxiliar.append("-")
        reporte.append(auxiliar)
    estudiantes = Estudiante.objects.filter(inscrito_gestion='si',anio_cursado__in=anios)
    numero_total=estudiantes.count()
    if reporte:
        return Response({"datos":reporte,"TOTAL":numero_total})
    else:
        return Response({"message": "no se encontró ningún estudiante, ingrese datos válidos"})