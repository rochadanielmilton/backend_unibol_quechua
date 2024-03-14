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
    estudiante=Estudiante.objects.filter(codigo_carrera=codigo_carrera,anio_cursado=anio_cursado, inscrito_gestion='si')
    nombre_carrera=Carrera.objects.filter(codigo_carrera=codigo_carrera).first().nombre_carrera
    numero_estudiantes=Count(estudiante)
    estudiante_serializer=EstudianteCarreraAnioSerializer(estudiante,many=True).data
    return Response({"año":anio_cursado,
                     "carrera":nombre_carrera,
                     "numero_estudiantes":numero_estudiantes,
                     "estudiantes":estudiante_serializer})