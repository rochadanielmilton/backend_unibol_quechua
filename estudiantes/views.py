from django.shortcuts import render
from rest_framework import viewsets
from parametros.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view



class MallaAcademicaView(viewsets.ModelViewSet):
    queryset=MallaAcademica.objects.all()
    serializer_class=MallaAcademicaSerializer

class EstudianteView(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()    
    serializer_class = EstudianteSerializer

class DocumentacionEstudianteView(viewsets.ModelViewSet):
    queryset=DocumentacionEstudiante.objects.all()
    serializer_class=DocumentacionEstudianteSerializer

class OrganizacionView(viewsets.ModelViewSet):
    queryset=Organizacion.objects.all()
    serializer_class=OrganizacionSerializer

class ResponsableEstudianteView(viewsets.ModelViewSet):
    queryset=ResponsableEstudiante.objects.all()
    serializer_class=ResponsableEstudianteSerializer

class EducacionPrimariaView(viewsets.ModelViewSet):
    queryset=EducacionPrimaria.objects.all()
    serializer_class=EducacionPrimariaSerializer

class AsignaturaCursadaView(viewsets.ModelViewSet):
    queryset=AsignaturaCursada.objects.all()
    serializer_class=AsignaturaCursadaSerializer

class NotaEstudianteView(viewsets.ModelViewSet):
    queryset=NotaEstudiante.objects.all()
    serializer_class=NotaEstudianteSerializer
    
@api_view(['GET']) 
def ObenerAsignaturasNoCursadas(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante).first()
    asignaturas_cursadas = AsignaturaCursada.objects.filter(ci_estudiante=estudiante.ci_estudiante)
    #print("------------------", asignaturas_cursadas.values_list('codigo_asignatura', flat=True))
    lista_asignaturas_aprobadas = []

    for asig in asignaturas_cursadas:        
        concluido = asig.estado_gestion_espaniol
        if concluido == 'APROBADO':
            lista_asignaturas_aprobadas.append(asig.id_malla_academica.codigo_asignatura_id)
            print("WWWWWWWWWWWW",asig.id_malla_academica.codigo_asignatura_id)
        #print("QQQQQQQQQQQQQQ",codigo_asignatura_concluida,"---", concluido)


    malla_estudiante=MallaAcademica.objects.filter(codigo_carrera=estudiante.codigo_carrera).exclude(codigo_asignatura__in=lista_asignaturas_aprobadas)
    serializer_malla=MallaAcademicaSerializer(malla_estudiante,many=True).data
    #serializer_asignaturas=AsignaturaCursadaSerializer(asignaturas_cursadas,many=True).data
    #malla=MallaAcademica.objects.get(id=30)
    # print("EEEEEEEEEEEEEE",malla.codigo_carrera)
    return Response(serializer_malla)
