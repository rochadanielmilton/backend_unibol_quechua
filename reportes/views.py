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
    
# @api_view(['GET'])
# def EstudiantesInscritosGenero(request):
#     reporte=[]

#     estudiante=Estudiante.objects.filter(codigo_carrera='AGRF',genero=genero, inscrito_gestion='si')
#     nombre_carrera=Carrera.objects.filter(codigo_carrera=codigo_carrera).first().nombre_carrera
#     if estudiante:
#         numero_estudiantes=estudiante.count()
#         estudiante_serializer=EstudianteCarreraAnioSerializer(estudiante,many=True).data
#         return Response({"año":anio_cursado,
#                         "carrera":nombre_carrera,
#                         "numero_estudiantes":numero_estudiantes,
#                         "estudiantes":estudiante_serializer})
#     else:
#         return Response({"message":"no se encontro ningun estudiante ingrese datos validos"})