from django.shortcuts import render
from rest_framework import viewsets
from parametros.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Avg, Count, F
from rest_framework import status

class EstudianteView(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()    
    serializer_class = EstudianteSerializer

#==========================ASIGANTUARAS NO CURSADAS PARA LA INSCRIPCION DE ESTUDIANTES==================== 
@api_view(['GET']) 
def ObenerAsignaturasNoCursadas(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante).first()
    if estudiante:
        asignaturas_cursadas = AsignaturaCursada.objects.filter(ci_estudiante=estudiante.ci_estudiante)
        lista_asignaturas_aprobadas = []

        for asig in asignaturas_cursadas:        
            concluido = asig.estado_gestion_espaniol
            if concluido == 'APROBADO':
                lista_asignaturas_aprobadas.append(asig.id_malla_academica.codigo_asignatura.codigo_asignatura)

        malla_estudiante=MallaAcademica.objects.filter(codigo_carrera=estudiante.codigo_carrera).exclude(codigo_asignatura__in=lista_asignaturas_aprobadas)
        print("WWWWWWWWWWWW",malla_estudiante)
        serializer_malla=MallaAcademicaInscripcionSerializer(malla_estudiante,many=True).data
        serializer_estudiante=EstudianteInscripcionSerializer(estudiante).data
        return Response({"estudiante":serializer_estudiante,"oferta_materias":serializer_malla})
    else:
        return Response({"message":"el estudiante con ci ingresado no existe"})
    
@api_view(['GET']) 
def ObtenerEstudiantesInscripcion(request):
    estudiantes=Estudiante.objects.filter(estado='habilitado',baja='no')
    estudiante_serializer=EstudianteInscripcionSerializer(estudiantes, many=True).data
    if estudiantes:
        return Response(estudiante_serializer,status=status.HTTP_200_OK)       
    else:
        return Response({"message":"error al optener los estudantes"},status=status.HTTP_400_BAD_REQUEST)
#================================================================================================================