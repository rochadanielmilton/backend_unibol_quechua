from django.shortcuts import render
from rest_framework import viewsets
from parametros.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Avg, Count, F

class AsignaturaView(viewsets.ModelViewSet):
    queryset=Asignatura.objects.all()
    serializer_class=AsignaturaSerializer

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
    lista_asignaturas_aprobadas = []

    for asig in asignaturas_cursadas:        
        concluido = asig.estado_gestion_espaniol
        if concluido == 'APROBADO':
            lista_asignaturas_aprobadas.append(asig.id_malla_academica.codigo_asignatura.codigo_asignatura)

    malla_estudiante=MallaAcademica.objects.filter(codigo_carrera=estudiante.codigo_carrera).exclude(codigo_asignatura__in=lista_asignaturas_aprobadas)
    print("WWWWWWWWWWWW",malla_estudiante)
    serializer_malla=MallaAcademicaSerializer(malla_estudiante,many=True).data

    return Response(serializer_malla)


@api_view(['GET'])
def ObtenerHitorialAcademico(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
    grado=VerificarGrado(ci_estudiante)
    fecha_hora=datetime.now()
    fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    otros_datos= estadisticas_materias(ci_estudiante)
    if not estudiante:
        return Response({"message":"El CI que ingreso no corresponde a ningun estudiante registrado"})
    else:
        estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante)
        serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
        return Response({"estudiante":estudiante_serializer,
                         "grado":grado,
                         "fecha_emision":fecha_emision,
                        "datos":serializer_asignaturas_cursadas,
                        "otros_datos":otros_datos
                        })


def estadisticas_materias(ci_estudiante):
    # Filtrar las asignaturas cursadas
    asignaturas_aprobadas = AsignaturaCursada.objects.filter(
    id_nota__resultado_gestion_espaniol='APROBADO',
    ci_estudiante=ci_estudiante
    )
    # Obtener la cantidad de asignaturas aprobadas
    cantidad_aprobadas = asignaturas_aprobadas.count()

    # Obtener el promedio de las notas finales de las asignaturas aprobadas
    promedio_aprobadas = asignaturas_aprobadas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']
    promedio_aprobadas_redondeado=round(promedio_aprobadas,2)

    # Obtener estadísticas de todas las materias cursadas
    asignaturas_aprobadas = AsignaturaCursada.objects.filter(
    ci_estudiante=ci_estudiante
    )
    cantidad_todas = asignaturas_aprobadas.count()
    promedio_todas = asignaturas_aprobadas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']
    promedio_todas_redondedado=round(promedio_todas,2)

    return {
        'cantidad_aprobadas': cantidad_aprobadas,
        'promedio_aprobadas': promedio_aprobadas_redondeado,
        'cantidad_todas': cantidad_todas,
        'promedio_todas': promedio_todas_redondedado,
    }

# @api_view(['GET'])    
# def ActualizarNotas(request):
#     notas=NotaEstudiante.objects.all()
#     for nota in notas:
#         asignatura=AsignaturaCursada.objects.get(id=nota.id_asignatura_cursada.id)
#         asignatura.id_nota=nota.id
#         asignatura.save()
#     return Response({"message":"exitoso"})

def VerificarGrado(ci_estudiante):
    asignaturas_cursadas = AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).values_list('codigo_asignatura', flat=True)
    asignaturas_licenciatura = AsignaturasLicenciatura.objects.values_list('codigo_asignatura', flat=True)
    
    resultado = 'TÉCNICO SUPERIOR'

    for asignatura_cursada in asignaturas_cursadas:
        if asignatura_cursada in asignaturas_licenciatura:
            resultado = 'LICENCIATURA'
            break  # Termina la iteración tan pronto como se encuentra una coincidencia

    return resultado

@api_view(['GET'])
def ObtenerMateriasAprobadas(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
    grado=VerificarGrado(ci_estudiante)
    fecha_hora=datetime.now()
    fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
    otros_datos= estadisticas_materias_aprobadas(ci_estudiante)
    if not estudiante:
        return Response({"message":"El CI que ingreso no corresponde a ningun estudiante registrado"})
    else:
        estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante,estado_gestion_espaniol='APROBADO')
        serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
        return Response({"estudiante":estudiante_serializer,
                         "grado":grado,
                         "fecha_emision":fecha_emision,
                        "datos":serializer_asignaturas_cursadas,
                        "otros_datos":otros_datos
                        })
def estadisticas_materias_aprobadas(ci_estudiante):
    # Filtrar las asignaturas cursadas que tienen una nota final aprobada
    asignaturas_aprobadas = AsignaturaCursada.objects.filter(
    id_nota__resultado_gestion_espaniol='APROBADO',
    ci_estudiante=ci_estudiante
    )
    # Obtener la cantidad de asignaturas aprobadas
    cantidad_aprobadas = asignaturas_aprobadas.count()

    # Obtener el promedio de las notas finales de las asignaturas aprobadas
    promedio_aprobadas = asignaturas_aprobadas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']
    promedio_aprobadas_redondeado=round(promedio_aprobadas,2)

    return {
        'cantidad_aprobadas': cantidad_aprobadas,
        'promedio_aprobadas': promedio_aprobadas_redondeado,

    }