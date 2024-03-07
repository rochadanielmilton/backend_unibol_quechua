from django.shortcuts import render
from rest_framework import viewsets
from parametros.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Avg, Count, F
from rest_framework import status
from django.db.models import Max

class AsignaturaView(viewsets.ModelViewSet):
    queryset=Asignatura.objects.all()
    serializer_class=AsignaturaSerializer

class EstudianteView(viewsets.ModelViewSet):
    queryset = Estudiante.objects.filter(estado='habilitado',baja='no').order_by('anio_ingreso')   
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
def ObtenerHitorialAcademico(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
    if estudiante:
        
        grado=VerificarGrado(ci_estudiante)
        fecha_hora=datetime.now()
        fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
               
       
        estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).order_by('anio_cursado')
        if asignaturas_cursadas:
            otros_datos= estadisticas_materias(ci_estudiante)
            serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
            return Response({"estudiante":estudiante_serializer,
                    "grado":grado,
                    "fecha_emision":fecha_emision,
                    "datos":serializer_asignaturas_cursadas,
                    "otros_datos":otros_datos
                    })
        else:
            return Response({"message":"El estudiante no cuenta con ninguna materia registrada"})
    else:
        return Response({"Message":"El ci ingresado no coincide con ningun registro"})


@api_view(['GET'])
def ObtenerHitorialAcademico2(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
    if estudiante:
        
        grado=VerificarGrado(ci_estudiante)
        fecha_hora=datetime.now()
        fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
               
        materias_tomadas=[]
        estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).order_by('anio_cursado')
        for asignatura in asignaturas_cursadas:
            materias_tomadas.append(asignatura.codigo_asignatura)
            if asignatura.malla_aplicada=='2018' and asignatura.homologacion=='SI':
                nombre_asignatura=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_malla_ajustada).nombre_asignatura
                materias_tomadas.append(nombre_asignatura)
                
            elif asignatura.malla_aplicada=='2018'and  asignatura.homologacion=='NO':
                nombre_asignatura=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura).asignatura_malla_2018
                materias_tomadas.append(nombre_asignatura)
            elif asignatura.malla_aplicada=='2023':
                nombre_asignatura=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura).nombre_asignatura
                materias_tomadas.append(nombre_asignatura)
            print("------------",asignatura.codigo_asignatura,' = ',nombre_asignatura)

        # if asignaturas_cursadas:
        #     otros_datos= estadisticas_materias(ci_estudiante)
        #     serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
        #     return Response({"estudiante":estudiante_serializer,
        #             "grado":grado,
        #             "fecha_emision":fecha_emision,
        #             "datos":serializer_asignaturas_cursadas,
        #             "otros_datos":otros_datos
        #             })
        # else:
        #     return Response({"message":"El estudiante no cuenta con ninguna materia registrada"})
        
        return Response({"estudiante":estudiante_serializer,
                     "grado":grado,
                     "fecha_emision":fecha_emision,
                     #"datos":serializer_asignaturas_cursadas,
                     #"otros_datos":otros_datos
                     })
    else:
        return Response({"Message":"El ci ingresado no coincide con ningun registro"})


def estadisticas_materias(ci_estudiante):
    # Filtrar las asignaturas cursadas
    asignaturas_aprobadas = AsignaturaCursada.objects.filter(id_nota__resultado_gestion_espaniol='APR.',ci_estudiante=ci_estudiante)
    if asignaturas_aprobadas: 
        cantidad_aprobadas = asignaturas_aprobadas.count()
        # Obtener el promedio de las notas finales de las asignaturas aprobadas
        promedio_aprobadas = asignaturas_aprobadas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']
        if promedio_aprobadas:
            promedio_aprobadas_redondeado=round(promedio_aprobadas,2)
        else:
            promedio_aprobadas_redondeado=0
    else:
        cantidad_aprobadas=0
        promedio_aprobadas_redondeado=0

        # Obtener estadísticas de todas las materias cursadas
    asignaturas_todas = AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante)
    if asignaturas_todas:
        cantidad_todas = asignaturas_todas.count()
        promedio_todas = asignaturas_todas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']  
        
        if promedio_todas:
            promedio_todas_redondedado=round(promedio_todas,2)
        else:
            promedio_todas_redondedado=0
    else:
        cantidad_todas=0
        promedio_todas_redondedado=0

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

def actualizar_anio_cursado(ci_estudiante):
    asignaturas_aprobadas = AsignaturaCursada.objects.filter(
    ci_estudiante=ci_estudiante
    )

@api_view(['GET'])
def subirNota(request,ci_estudiante):
    estudiante = Estudiante.objects.get(ci_estudiante=ci_estudiante)
    asignatura_cursado=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante,codigo_asignatura='TSAC 101')
    #nota=NotaEstudiante.objects.get()
    asignatura_serializer=AsignaturaCursadaNotaSerializer(asignatura_cursado, many=True).data
    return Response(asignatura_serializer)

@api_view(['GET'])
def formularioAdmision(request,ci_estudiante):
    gestion_actual=str(datetime.now().year)
    obtenerUltimo_numero_registrado('ACUC')
    numero_archivo=obtenerNumeroArchivo(ci_estudiante)
    try:
        estudiante=Estudiante.objects.get(ci_estudiante=ci_estudiante)
        if estudiante.anio_ingreso==gestion_actual:
            requisitos=RequisitosInscripcion.objects.filter(tipo='NUEVO',estado='habilitado').values('requisito')
        else:
            requisitos=RequisitosInscripcion.objects.filter(tipo='REGULAR',estado='habilitado').values('requisito')
        estudiante_serializer= EstudianteSerializerFormularioAdmision(estudiante).data
        return Response({'gestion':gestion_actual,
                         'datos_estudiante':estudiante_serializer,
                         'requisitos':requisitos,
                         'numero_archivo':numero_archivo})
    except:
        return Response({'message':'No se encuentra el ci ingresado'})
    
def obtenerNumeroArchivo(ci_estudiante):
    estudiante=Estudiante.objects.get(ci_estudiante=ci_estudiante)
    return estudiante.numero_archivo

def obtenerUltimo_numero_registrado(codigo_carrera):
    if codigo_carrera=='ACUC':
        ultimo_estudiante = Estudiante.objects.filter(codigo_carrera=codigo_carrera).exclude(numero_archivo__in=[370, 495]).aggregate(max_numero_archivo=Max('numero_archivo'))['max_numero_archivo']
        print("------------",ultimo_estudiante)
    else:
        ultimo_estudiante=Estudiante.objects.filter(codigo_carrera=codigo_carrera).aggregate(max_numero_archivo=Max('numero_archivo'))['max_numero_archivo'] 
        print("------------",ultimo_estudiante)
    return ultimo_estudiante

@api_view(['GET'])
def obtenerCertificacionGestionAnterior(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
    if estudiante:
        
        grado=VerificarGrado(ci_estudiante)
        fecha_hora=datetime.now()
        fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        anio_anterior = str(datetime.now().year-1)
               
       
        estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante,anio_cursado=anio_anterior )
        if asignaturas_cursadas:
            #otros_datos= estadisticas_materias(ci_estudiante)
            serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
            return Response({"estudiante":estudiante_serializer,
                    "grado":grado,
                    "fecha_emision":fecha_emision,
                    "datos":serializer_asignaturas_cursadas                    
                    })
        else:
            return Response({"message":"El estudiante no cuenta con ninguna materia registrada"})
    else:
        return Response({"Message":"El ci ingresado no coincide con ningun registro"})