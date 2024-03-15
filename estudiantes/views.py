from django.shortcuts import render
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

class AsignaturaView(viewsets.ModelViewSet):
    queryset=Asignatura.objects.all()
    serializer_class=AsignaturaSerializer

#@permission_classes([IsAuthenticated])
class EstudianteRegularesView(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    anio_actual=str(datetime.now().year)
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
    


# @api_view(['GET'])
# def ObtenerHitorialAcademico(request,ci_estudiante):
#     estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
#     if estudiante:
        
#         grado=VerificarGrado(ci_estudiante)
#         fecha_hora=datetime.now()
#         fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
               
       
#         estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
#         asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).order_by('anio_cursado')
#         if asignaturas_cursadas:
#             otros_datos= estadisticas_materias(ci_estudiante)
#             serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
#             return Response({"estudiante":estudiante_serializer,
#                     "grado":grado,
#                     "fecha_emision":fecha_emision,
#                     "datos":serializer_asignaturas_cursadas,
#                     "otros_datos":otros_datos
#                     })
#         else:
#             return Response({"message":"El estudiante no cuenta con ninguna materia registrada"})
#     else:
#         return Response({"Message":"El ci ingresado no coincide con ningun registro"})


@api_view(['GET'])
def ObtenerHitorialAcademico2(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante).first()
    if estudiante:
        #print("+++++++++++",estudiante.codigo_carrera)   and estudiante.codigo_carrera.codigo_carrera!='TIAL'
        grado=VerificarGrado(ci_estudiante)
        fecha_hora=datetime.now()
        fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
               
        materias_tomadas=[]
        estudiante_serializer=EstudianteHistorialSerializer(estudiante).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).order_by('anio_cursado')
        otros_datos= estadisticas_materias_malla_2023(ci_estudiante)
        total_horas_vencidas=0
        for asignatura in asignaturas_cursadas:
            auxiliar=[]
            if asignatura.malla_aplicada=='2018' and asignatura.homologacion=='SI':
                auxiliar.append(asignatura.anio_cursado)
                auxiliar.append(asignatura.codigo_malla_ajustada)
                materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_malla_ajustada)             
                auxiliar.append(materia.nombre_asignatura)
                auxiliar.append(materia.total_horas)
                total_horas_vencidas=total_horas_vencidas+materia.total_horas
                auxiliar.append((materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1)
                auxiliar.append(asignatura.id_nota.nota_num_final)
                auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                if asignatura.convalidacion:
                    auxiliar.append('CONV.HOMOLOGADO')
                else:
                    auxiliar.append(asignatura.homologacion)
                materias_tomadas.append(auxiliar)
                #print(asignatura.anio_cursado," - ",asignatura.codigo_malla_ajustada," = ",materia.nombre_asignatura," = ", materia.total_horas," = ",(materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1," = ",asignatura.id_nota.nota_num_final," = ",asignatura.id_nota.resultado_gestion_espaniol," = ",asignatura.homologacion)
                
            # elif asignatura.malla_aplicada=='2018'and  asignatura.homologacion=='NO':
            #     auxiliar.append(asignatura.anio_cursado)
            #     auxiliar.append(asignatura.codigo_asignatura)
            #     materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura)
            #     auxiliar.append(materia.asignatura_malla_2018)
            #     auxiliar.append(materia.total_horas)
            #     auxiliar.append((materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1)
            #     auxiliar.append(asignatura.id_nota.nota_num_final)
            #     auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
            #     auxiliar.append(asignatura.homologacion)
            #     materias_tomadas.append(auxiliar)
            #     print(asignatura.anio_cursado," - ",asignatura.codigo_asignatura," = ",materia.asignatura_malla_2018," = ", materia.total_horas," = ",(materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1," = ",asignatura.id_nota.nota_num_final," = ",asignatura.id_nota.resultado_gestion_espaniol," = ",asignatura.homologacion)
            elif asignatura.malla_aplicada=='2023' and asignatura.estado_gestion_espaniol!='ABANDONO':
                auxiliar.append(asignatura.anio_cursado)
                auxiliar.append(asignatura.codigo_asignatura)
                materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura)
                auxiliar.append(materia.nombre_asignatura)
                auxiliar.append(materia.total_horas)
                total_horas_vencidas=total_horas_vencidas+materia.total_horas
                auxiliar.append((materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1)
                auxiliar.append(asignatura.id_nota.nota_num_final)
                auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                if asignatura.convalidacion:
                    auxiliar.append('CONV.Segun RM 0155/2023')
                else:
                    auxiliar.append("Segun RM 0155/2023")
                materias_tomadas.append(auxiliar)
          
        return Response({"estudiante":estudiante_serializer,
                     "grado":grado,
                     "fecha_emision":fecha_emision,
                     "datos":materias_tomadas,
                     "otros_datos":otros_datos,
                     "total_horas_vencidas":total_horas_vencidas
                     #"datos":serializer_asignaturas_cursadas,
                     
                     })
    else:
        return Response({"Message":"El ci ingresado no coincide con ningun registro"})
    
@api_view(['GET'])
def ObtenerHitorialAcademicoAvanceGeneral(request,ci_estudiante):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante).first()
    if estudiante:
        #print("+++++++++++",estudiante.codigo_carrera)   and estudiante.codigo_carrera.codigo_carrera!='TIAL'
        grado=VerificarGrado(ci_estudiante)
        fecha_hora=datetime.now()
        fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
               
        materias_tomadas=[]
        estudiante_serializer=EstudianteHistorialSerializer(estudiante).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).order_by('anio_cursado')
        otros_datos= estadisticas_materias_general(ci_estudiante)
        for asignatura in asignaturas_cursadas:
            auxiliar=[]
            if asignatura.malla_aplicada=='2018' and asignatura.homologacion=='SI':
                auxiliar.append(asignatura.anio_cursado)
                auxiliar.append(asignatura.codigo_malla_ajustada)
                materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_malla_ajustada)             
                auxiliar.append(materia.nombre_asignatura)
                auxiliar.append(materia.total_horas)
                auxiliar.append((materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1)
                auxiliar.append(asignatura.id_nota.nota_num_final)
                auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                if asignatura.convalidacion:
                    auxiliar.append('CONV.HOMOLOGADO')
                else:
                    auxiliar.append(asignatura.homologacion)
                materias_tomadas.append(auxiliar)
                #print(asignatura.anio_cursado," - ",asignatura.codigo_malla_ajustada," = ",materia.nombre_asignatura," = ", materia.total_horas," = ",(materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1," = ",asignatura.id_nota.nota_num_final," = ",asignatura.id_nota.resultado_gestion_espaniol," = ",asignatura.homologacion)
                
            elif asignatura.malla_aplicada=='2018'and  asignatura.homologacion=='NO':
                auxiliar.append(asignatura.anio_cursado)
                auxiliar.append(asignatura.codigo_asignatura)
                materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura)
                auxiliar.append(materia.asignatura_malla_2018)
                auxiliar.append(materia.total_horas)
                auxiliar.append((materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1)
                auxiliar.append(asignatura.id_nota.nota_num_final)
                auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                auxiliar.append(asignatura.homologacion)
                materias_tomadas.append(auxiliar)
            #     print(asignatura.anio_cursado," - ",asignatura.codigo_asignatura," = ",materia.asignatura_malla_2018," = ", materia.total_horas," = ",(materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1," = ",asignatura.id_nota.nota_num_final," = ",asignatura.id_nota.resultado_gestion_espaniol," = ",asignatura.homologacion)
            elif asignatura.malla_aplicada=='2023' and asignatura.estado_gestion_espaniol!='ABANDONO':
                auxiliar.append(asignatura.anio_cursado)
                auxiliar.append(asignatura.codigo_asignatura)
                materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura)
                auxiliar.append(materia.nombre_asignatura)
                auxiliar.append(materia.total_horas)
                auxiliar.append((materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1)
                auxiliar.append(asignatura.id_nota.nota_num_final)
                auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                if asignatura.convalidacion:
                    auxiliar.append('CONV.Segun RM 0155/2023')
                else:
                    auxiliar.append("Segun RM 0155/2023")
                materias_tomadas.append(auxiliar)
          
        return Response({"estudiante":estudiante_serializer,
                     "grado":grado,
                     "fecha_emision":fecha_emision,
                     "datos":materias_tomadas,
                     "otros_datos":otros_datos
                     #"datos":serializer_asignaturas_cursadas,
                     
                     })
    else:
        return Response({"Message":"El ci ingresado no coincide con ningun registro"})

def estadisticas_materias_malla_2023(ci_estudiante):
    # Filtrar las asignaturas cursadas
    asignaturas_aprobadas = AsignaturaCursada.objects.filter(id_nota__resultado_gestion_espaniol='APR.',ci_estudiante=ci_estudiante).exclude(homologacion='NO',malla_aplicada='2018')
    if asignaturas_aprobadas:
        cantidad_aprobadas = asignaturas_aprobadas.count()
        print("-------", cantidad_aprobadas)
        # Obtener el promedio de las notas finales de las asignaturas aprobadas
        promedio_aprobadas = asignaturas_aprobadas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']
        
        if promedio_aprobadas:
            promedio_aprobadas_redondeado=round(promedio_aprobadas,2)
            print("-------", promedio_aprobadas_redondeado)
        else:
            promedio_aprobadas_redondeado=0
    else:
        cantidad_aprobadas=0
        promedio_aprobadas_redondeado=0

        # Obtener estadísticas de todas las materias cursadas
    asignaturas_todas = AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).exclude(homologacion='NO',malla_aplicada='2018').exclude(estado_gestion_espaniol='ABANDONO')
    if asignaturas_todas:
        cantidad_todas = asignaturas_todas.count()
        print("-------", cantidad_todas)
        promedio_todas = asignaturas_todas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']  
        
        if promedio_todas:
            promedio_todas_redondedado=round(promedio_todas,2)
            print("-------", promedio_todas_redondedado)
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

def estadisticas_materias_general(ci_estudiante):
    # Filtrar las asignaturas cursadas
    asignaturas_aprobadas = AsignaturaCursada.objects.filter(id_nota__resultado_gestion_espaniol='APR.',ci_estudiante=ci_estudiante)
    if asignaturas_aprobadas:
        cantidad_aprobadas = asignaturas_aprobadas.count()
        print("-------", cantidad_aprobadas)
        # Obtener el promedio de las notas finales de las asignaturas aprobadas
        promedio_aprobadas = asignaturas_aprobadas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']
        
        if promedio_aprobadas:
            promedio_aprobadas_redondeado=round(promedio_aprobadas,2)
            print("-------", promedio_aprobadas_redondeado)
        else:
            promedio_aprobadas_redondeado=0
    else:
        cantidad_aprobadas=0
        promedio_aprobadas_redondeado=0

        # Obtener estadísticas de todas las materias cursadas
    asignaturas_todas = AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).exclude(estado_gestion_espaniol='ABANDONO')
    if asignaturas_todas:
        cantidad_todas = asignaturas_todas.count()
        print("-------", cantidad_todas)
        promedio_todas = asignaturas_todas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']  
        
        if promedio_todas:
            promedio_todas_redondedado=round(promedio_todas,2)
            print("-------", promedio_todas_redondedado)
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
    asignaturas_cursadas = AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).exclude(estado_gestion_espaniol='ABANDONO').values_list('codigo_asignatura', flat=True)
    asignaturas_licenciatura = AsignaturasLicenciatura.objects.values_list('codigo_asignatura', flat=True)
    print("--------",asignaturas_cursadas)
    resultado = 'TÉCNICO SUPERIOR'

    for asignatura_cursada in asignaturas_cursadas:
        if asignatura_cursada in asignaturas_licenciatura:
            resultado = 'LICENCIATURA'
            break  # Termina la iteración tan pronto como se encuentra una coincidencia

    return resultado

# @api_view(['GET'])
# def ObtenerMateriasAprobadas(request,ci_estudiante):
#     estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
#     grado=VerificarGrado(ci_estudiante)
#     fecha_hora=datetime.now()
#     fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
#     otros_datos= estadisticas_materias_aprobadas(ci_estudiante)
#     if not estudiante:
#         return Response({"message":"El CI que ingreso no corresponde a ningun estudiante registrado"})
#     else:
#         estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
#         asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante,estado_gestion_espaniol='APROBADO')
#         serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
#         return Response({"estudiante":estudiante_serializer,
#                          "grado":grado,
#                          "fecha_emision":fecha_emision,
#                         "datos":serializer_asignaturas_cursadas,
#                         "otros_datos":otros_datos
#                         })
# def estadisticas_materias_aprobadas(ci_estudiante):
#     # Filtrar las asignaturas cursadas que tienen una nota final aprobada
#     asignaturas_aprobadas = AsignaturaCursada.objects.filter(
#     id_nota__resultado_gestion_espaniol='APROBADO',
#     ci_estudiante=ci_estudiante
#     )
#     # Obtener la cantidad de asignaturas aprobadas
#     cantidad_aprobadas = asignaturas_aprobadas.count()

#     # Obtener el promedio de las notas finales de las asignaturas aprobadas
#     promedio_aprobadas = asignaturas_aprobadas.aggregate(Avg('id_nota__nota_num_final'))['id_nota__nota_num_final__avg']
#     promedio_aprobadas_redondeado=round(promedio_aprobadas,2)

#     return {
#         'cantidad_aprobadas': cantidad_aprobadas,
#         'promedio_aprobadas': promedio_aprobadas_redondeado,

#     }

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

# @api_view(['GET'])
# def obtenerCertificacionGestionAnterior(request,ci_estudiante):
#     estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
#     if estudiante:
        
#         grado=VerificarGrado(ci_estudiante)
#         fecha_hora=datetime.now()
#         fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
#         anio_anterior = str(datetime.now().year-1)
               
       
#         estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
#         asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante,anio_cursado=anio_anterior )
#         if asignaturas_cursadas:
#             #otros_datos= estadisticas_materias(ci_estudiante)
#             serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
#             return Response({"estudiante":estudiante_serializer,
#                     "grado":grado,
#                     "fecha_emision":fecha_emision,
#                     "datos":serializer_asignaturas_cursadas                    
#                     })
#         else:
#             return Response({"message":"El estudiante no cuenta con ninguna materia registrada"})
#     else:
#         return Response({"Message":"El ci ingresado no coincide con ningun registro"})
 
@api_view(['GET'])
def obtenerCertificacionPorGestion(request,ci_estudiante,anio):
    estudiante=Estudiante.objects.filter(ci_estudiante=ci_estudiante)
    if estudiante:
        
        grado=VerificarGrado(ci_estudiante)
        fecha_hora=datetime.now()
        fecha_emision = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        #anio_anterior = str(datetime.now().year-1)
               
       
        estudiante_serializer=EstudianteHistorialSerializer(estudiante.first()).data
        asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante,anio_cursado=anio ).order_by('codigo_asignatura')
        if asignaturas_cursadas:
            materias_tomadas=[]
            cont=1
            for asignatura in asignaturas_cursadas:
                auxiliar=[]
                if asignatura.malla_aplicada=='2018' and asignatura.homologacion=='SI':
                    auxiliar.append(cont)
                    auxiliar.append(asignatura.anio_cursado)
                    auxiliar.append(asignatura.codigo_malla_ajustada)
                    materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_malla_ajustada)             
                    auxiliar.append(materia.nombre_asignatura)
                    auxiliar.append(asignatura.id_nota.nota_num_final)
                    auxiliar.append(asignatura.id_nota.nota_literal_quechua)
                    auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                    # if asignatura.convalidacion:
                    #     auxiliar.append('CONV.HOMOLOGADO')
                    # else:
                    #     auxiliar.append('HOMOLOGADO')
                    materias_tomadas.append(auxiliar)
                    cont=cont+1
                    
                    #print(asignatura.anio_cursado," - ",asignatura.codigo_malla_ajustada," = ",materia.nombre_asignatura," = ", materia.total_horas," = ",(materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1," = ",asignatura.id_nota.nota_num_final," = ",asignatura.id_nota.resultado_gestion_espaniol," = ",asignatura.homologacion)
                
                elif asignatura.malla_aplicada=='2018'and  asignatura.homologacion=='NO':
                    auxiliar.append(cont)
                    auxiliar.append(asignatura.anio_cursado)
                    auxiliar.append(asignatura.codigo_asignatura)
                    materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura)
                    auxiliar.append(materia.asignatura_malla_2018)
                    auxiliar.append(asignatura.id_nota.nota_num_final)
                    auxiliar.append(asignatura.id_nota.nota_literal_quechua)
                    auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                    # auxiliar.append('NO HOMOLOGADO')
                    materias_tomadas.append(auxiliar)
                    cont=cont+1
                    #print(asignatura.anio_cursado," - ",asignatura.codigo_asignatura," = ",materia.asignatura_malla_2018," = ", materia.total_horas," = ",(materia.pre_requisito1+","+materia.pre_requisito2) if materia.pre_requisito2 else materia.pre_requisito1," = ",asignatura.id_nota.nota_num_final," = ",asignatura.id_nota.resultado_gestion_espaniol," = ",asignatura.homologacion)
                elif asignatura.malla_aplicada=='2023' and asignatura.estado_gestion_espaniol!='ABANDONO':
                    auxiliar.append(cont)
                    auxiliar.append(asignatura.anio_cursado)
                    auxiliar.append(asignatura.codigo_asignatura)
                    materia=Asignatura.objects.get(codigo_asignatura=asignatura.codigo_asignatura)
                    auxiliar.append(materia.nombre_asignatura)
                    auxiliar.append(asignatura.id_nota.nota_num_final)
                    auxiliar.append(asignatura.id_nota.nota_literal_quechua)
                    auxiliar.append(asignatura.id_nota.resultado_gestion_espaniol)
                    # if asignatura.convalidacion:
                    #     auxiliar.append('CONV.Segun RM 0155/2023')
                    # else:
                    #     auxiliar.append("Segun RM 0155/2023")
                    materias_tomadas.append(auxiliar)
                    cont=cont+1
            #otros_datos= estadisticas_materias(ci_estudiante)
            serializer_asignaturas_cursadas=AsignaturaCursadaSerializer(asignaturas_cursadas, many=True).data
            return Response({"estudiante":estudiante_serializer,
                    "grado":grado,
                    "fecha_emision":fecha_emision,
                    "datos":materias_tomadas                    
                    })
        else:
            return Response({"message":"El estudiante no cuenta con ninguna materia registrada en esa gestión"})
    else:
        return Response({"Message":"El ci ingresado no coincide con ningun registro"})
    
@api_view(['GET'])
def ObtenerEducacionPrimaria(request,ci_estudiante):
    educacion_primaria=EducacionPrimaria.objects.filter(ci_estudiante=ci_estudiante).first()
    if educacion_primaria:
        educacion_primaria_serializer=EducacionPrimariaSerializer(educacion_primaria).data
    else:
        educacion_primaria_serializer={}
    return Response(educacion_primaria_serializer)

@api_view(['GET'])
def ObtenerResponsable(request,ci_estudiante):
    responsable=ResponsableEstudiante.objects.filter(ci_estudiante=ci_estudiante).first()
    if responsable:
       responsable_serializer=ResponsableEstudianteSerializer(responsable).data
    else:
       responsable_serializer={}
    return Response(responsable_serializer)

@api_view(['GET'])
def ObtenerOrganizacion(request,ci_estudiante):
    organizacion=Organizacion.objects.filter(ci_estudiante=ci_estudiante).first()
    if organizacion:
        organizacion_serializer=OrganizacionSerializer(organizacion).data
    else:
        organizacion_serializer={}
    return Response(organizacion_serializer)
