from django.shortcuts import render
from rest_framework import viewsets
from parametros.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Avg, Count, F
from rest_framework import status
from django.db import transaction

class EstudianteView(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()    
    serializer_class = EstudianteSerializer


#=========================LISTA DE ESTUDIANTE PARA INSCRIPCION========================================
@api_view(['GET']) 
def ObtenerEstudiantesInscripcion(request):
    estudiantes=Estudiante.objects.filter(baja='no').order_by('-inscrito_gestion')
    estudiante_serializer=EstudianteInscripcionSerializer(estudiantes, many=True).data
    if estudiantes:
        return Response(estudiante_serializer,status=status.HTTP_200_OK)       
    else:
        return Response({"message":"error al optener los estudantes"},status=status.HTTP_400_BAD_REQUEST)

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

#================================================================================================================
@api_view(['POST']) 
def inscribirEstudiante(request):
    try:
        with transaction.atomic():
            data = request.data
            ci_estudiante = data.get('ci_estudiante')
            ids_mallas = data.get('ids_mallas')

            estudiante = Estudiante.objects.get(ci_estudiante=ci_estudiante)
            fecha_emision=datetime.now().date()
            

            if estudiante:
                if estudiante.inscrito_gestion=='no':
                    estudiante.inscrito_gestion='si'
                    estudiante.save()
                    for id_malla in ids_mallas:
                        malla = MallaAcademica.objects.get(id=id_malla)
                        nueva_asignatura_cursada = AsignaturaCursada.objects.create(
                            ci_estudiante=estudiante,
                            codigo_asignatura=malla.codigo_asignatura.codigo_asignatura,
                            id_malla_academica=malla,
                            anio_cursado=datetime.now().year,
                            estado_gestion_quechua='QHIPAKUN',
                            estado_gestion_espaniol='ABANDONO',
                            fecha_inscripcion=datetime.now(),
                            estado_inscripcion='inscrito'
                        )
                        nueva_nota=NotaEstudiante.objects.create(
                            id_asignatura_cursada=nueva_asignatura_cursada.id,
                            nota_num_gestion=0,
                            instancia='no',
                            nota_num_final=0,
                            resultado_gestion_espaniol='ABANDONO',
                            nota_literal_quechua="CH'USAQ",
                            resultado_gestion='QHIPAKUN',
                            gestion_cursada=datetime.now().year,
                            nivel_carrera=VerificarGrado(ci_estudiante)
                        )

                        if nueva_nota:
                            nueva_asignatura_cursada.id_nota=nueva_nota
                            nueva_asignatura_cursada.save()
                    asignaturas_malla=MallaAcademica.objects.filter(id__in=ids_mallas)
                    asignaturas_malla_serializer=MallaAcademicaInscripcionSerializer(asignaturas_malla,many=True).data
                    estudiante_serializer=EstudianteInscripcionSerializer(estudiante).data
                    numero_boleta=GenerarNuevaBoleta(estudiante.ci_estudiante)
                else:
                    return Response({"message":"El estudiante ya esta inscrito"})
                return Response({"estudiante": estudiante_serializer,
                                 "asignaturas_inscritas":asignaturas_malla_serializer,
                                 "fecha_emision":fecha_emision,
                                 "numero_boleta":numero_boleta,})
            else:
                return Response({"message": "El estudiante no se encuentra registrado"})
    except Exception as e:
        return Response({"error": str(e)})

    
def VerificarGrado(ci_estudiante):
    asignaturas_cursadas = AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).values_list('codigo_asignatura', flat=True)
    asignaturas_licenciatura = AsignaturasLicenciatura.objects.values_list('codigo_asignatura', flat=True)
    
    resultado = 'TS'

    for asignatura_cursada in asignaturas_cursadas:
        if asignatura_cursada in asignaturas_licenciatura:
            resultado = 'LC'
            break  # Termina la iteración tan pronto como se encuentra una coincidencia

    return resultado


def GenerarNuevaBoleta(ci_estudiante):
    ultimo_numero=BoletaInscripcion.objects.last()
    if ultimo_numero:
        nuevo_numero_boleta=ultimo_numero.numero_boleta+1
    else:
        nuevo_numero_boleta=1
    gestion=datetime.now().year
    nuevo_numero_boleta_str = str(nuevo_numero_boleta).zfill(4)
    BoletaInscripcion.objects.create(numero_boleta=nuevo_numero_boleta,ci_estudiante=ci_estudiante,gestion=gestion,emitido='si')
    return nuevo_numero_boleta_str
# @api_view(['POST'])
# def Recibir_Datos(request):
#     data = request.data
#     tag_leido = data['tag_leido']
#     placa=data['placa']
#     numero_ejes_inicio=data['numero_ejes_inicio']
#     numero_ejes_salida=data['numero_ejes_salida']
#     ancho_vehiculo=data['ancho_vehiculo']
#     alto_vehiculo=data['alto_vehiculo']
#     clase_vehiculo=data['clase_vehiculo']
#     imagen_frontal=data['imagen_frontal']
#     imagen_lateral=data['imagen_lateral']
#     estado = data['estado'] 