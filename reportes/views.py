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
    anios=['PRIMER AÑO', 'SEGUNDO AÑO', 'TERCER AÑO', 'CUARTO AÑO', 'QUINTO AÑO']
    reporte=[]

    estudiantes_varones=Estudiante.objects.filter(codigo_carrera='AGRF',genero='M', inscrito_gestion='si',anio_cursado__in=anios)
    numero_varones=estudiantes_varones.count()
    estudiantes_mujeres=Estudiante.objects.filter(codigo_carrera='AGRF',genero='F', inscrito_gestion='si',anio_cursado__in=anios)
    numero_mujeres=estudiantes_mujeres.count()
    carrera=Carrera.objects.get(codigo_carrera='AGRF')
    auxiliar=[carrera.nombre_carrera,numero_varones,numero_mujeres]
    reporte.append(auxiliar)

    estudiantes_varones=Estudiante.objects.filter(codigo_carrera='TIAL',genero='M', inscrito_gestion='si',anio_cursado__in=anios)
    numero_varones=estudiantes_varones.count()
    estudiantes_mujeres=Estudiante.objects.filter(codigo_carrera='TIAL',genero='F', inscrito_gestion='si',anio_cursado__in=anios)
    numero_mujeres=estudiantes_mujeres.count()
    carrera=Carrera.objects.get(codigo_carrera='TIAL')
    auxiliar=[carrera.nombre_carrera,numero_varones,numero_mujeres]
    reporte.append(auxiliar)

    estudiantes_varones=Estudiante.objects.filter(codigo_carrera='ECOP',genero='M', inscrito_gestion='si',anio_cursado__in=anios)
    numero_varones=estudiantes_varones.count()
    estudiantes_mujeres=Estudiante.objects.filter(codigo_carrera='ECOP',genero='F', inscrito_gestion='si',anio_cursado__in=anios)
    numero_mujeres=estudiantes_mujeres.count()
    carrera=Carrera.objects.get(codigo_carrera='ECOP')
    auxiliar=[carrera.nombre_carrera,numero_varones,numero_mujeres]
    reporte.append(auxiliar)

    estudiantes_varones=Estudiante.objects.filter(codigo_carrera='ACUC',genero='M', inscrito_gestion='si',anio_cursado__in=anios)
    numero_varones=estudiantes_varones.count()
    estudiantes_mujeres=Estudiante.objects.filter(codigo_carrera='ACUC',genero='F', inscrito_gestion='si',anio_cursado__in=anios)
    numero_mujeres=estudiantes_mujeres.count()
    carrera=Carrera.objects.get(codigo_carrera='ACUC')
    auxiliar=[carrera.nombre_carrera,numero_varones,numero_mujeres]
    reporte.append(auxiliar)

    estudiantes_varones=Estudiante.objects.filter(genero='M', inscrito_gestion='si',anio_cursado__in=anios)
    numero_varones=estudiantes_varones.count()
    estudiantes_mujeres=Estudiante.objects.filter(genero='F', inscrito_gestion='si',anio_cursado__in=anios)
    numero_mujeres=estudiantes_mujeres.count()
    auxiliar=["TOTAL VARONES Y MUJERES",numero_varones,numero_mujeres]
    reporte.append(auxiliar)

    if reporte:
        return Response(reporte)
    else:
        return Response({"message":"no se encontro ningun estudiante ingrese datos validos"})