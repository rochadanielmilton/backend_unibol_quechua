from django.shortcuts import render
from rest_framework import viewsets
from parametros.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime
from django.db.models import Avg, Count, F,Max
from rest_framework import status
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class EstudianteView(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()    
    serializer_class = EstudianteSerializer


#=========================LISTA DE ESTUDIANTE PARA INSCRIPCION========================================
@api_view(['GET']) 
def ObtenerEstudiantesInscripcion(request):
    estudiantes=Estudiante.objects.filter(baja='no').order_by('-anio_ingreso')
    estudiante_serializer=EstudianteInscripcionSerializer(estudiantes, many=True).data
    ultimo_año=str(datetime.now().year)
    if estudiantes:
        return Response({"estudiantes": estudiante_serializer,
                         "anio_actual":ultimo_año})       
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
            if concluido == 'APR.':
                lista_asignaturas_aprobadas.append(asig.id_malla_academica.codigo_asignatura.codigo_asignatura)
                lista_asignaturas_aprobadas.append(asig.convalidacion)
            if asig.codigo_asignatura=='TSAA 107' and asig.estado_gestion_espaniol=='REP.':
                if 'TSAA 107' in lista_asignaturas_aprobadas:
                    lista_asignaturas_aprobadas.remove('TSAA 107')

        malla_estudiante=MallaAcademica.objects.filter(codigo_carrera=estudiante.codigo_carrera).exclude(codigo_asignatura__in=lista_asignaturas_aprobadas)
        #print("WWWWWWWWWWWW",malla_estudiante)
        serializer_malla=MallaAcademicaInscripcionSerializer(malla_estudiante,many=True).data
        serializer_estudiante=EstudianteInscripcionSerializer(estudiante).data
        return Response({"estudiante":serializer_estudiante,                         
                         "oferta_materias":serializer_malla})
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

            anio_aterior=str(datetime.now().year-1)
            lista_asignaturas_anio_anterior=AsignaturaCursada.objects.filter(anio_cursado=anio_aterior,ci_estudiante=ci_estudiante).order_by('codigo_asignatura')
            lista_asignaturas_anio_anterior_serializer=AsignaturaCursadaAnioAnteriorSerializer(lista_asignaturas_anio_anterior,many=True).data
            #print("------------------",lista_asignaturas_anio_anterior_serializer)

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
                            estado_inscripcion='inscrito',
                            malla_aplicada='2023',
                            homologacion='NO',
                            cod_carrera=estudiante.codigo_carrera.codigo_carrera
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
                    numero_archivo=obtenerNumeroArchivo(estudiante.ci_estudiante)
                else:
                    return Response({"message":"El estudiante ya esta inscrito"})
                return Response({"estudiante": estudiante_serializer,
                                 "asignaturas_gestion_anterior":lista_asignaturas_anio_anterior_serializer,
                                 "asignaturas_inscritas":asignaturas_malla_serializer,
                                 "fecha_emision":fecha_emision,
                                 "numero_boleta":numero_boleta,
                                 'numero_archivo':numero_archivo})
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

#=======FUNCIONES PARA LA MIGRACION DE REGISTROS DE POSTALTE A ESTUDIANTES REGULARES====================
@api_view(['GET']) 
def ObtenerPostulates(request):
    postulantes=PostulantePrepa.objects.all().order_by('-registrado')
    postulante_serializer=PostulantePrepaSerializer(postulantes,many=True).data
    if postulantes:
        return Response(postulante_serializer,status=status.HTTP_200_OK)       
    else:
        return Response({"message":"error al optener los postulantes"},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET']) 
def RegistrarNueboEstudiante(request,ci_postulante):
    respuesta={}
    #------------registro de nuevo estudiante del curso preparatorio---------
    try:
        postulante=PostulantePrepa.objects.get(ci_postulante=ci_postulante)
        numero_registro=str(datetime.now().year)+str(datetime.now().month).zfill(2)+ str(ObtenerNumeroRegistro()).zfill(4)
        carrera_nueva=ObtenerCodigoCarrera(postulante.carrera)
        nuevo_estudiante=Estudiante.objects.create(ci_estudiante=ci_postulante,extencion=postulante.extension_ci,
                                                   codigo_carrera=carrera_nueva,
                                                   nombres=postulante.nombres_p,apellidoP=postulante.apellido_paterno_p,
                                                   apellidoM=postulante.apellido_materno_p,celular=int(postulante.telefono_postulante),
                                                   genero=postulante.genero,fecha_nacimiento=postulante.fecha_nacimiento,
                                                   depa_nacimiento=postulante.departamento_nacimiento,munic_nacimiento=postulante.municipio_nacimiento,
                                                   tipo_ingreso=postulante.tipo_ingreso,estado_civil=postulante.estadocivil,
                                                   idioma_nativo=postulante.lengua_que_habla,email=postulante.email_postulante,
                                                   anio_ingreso=(datetime.now().year),
                                                   numero_archivo=obtenerUltimoNumeroRegistrado(carrera_nueva.codigo_carrera),homologacion='no',
                                                   convalidacion='no',egresado='no',titulado='no',estado='habilitado',baja='no',
                                                   numero_registro=numero_registro,anio_cursado='PRIMER AÑO',inscrito_gestion='no')
        if nuevo_estudiante:                                           
            respuesta['Estudiante']='Se registro los datos del estudiante correctamente'
            postulante.registrado='si'
            postulante.save()
    #--------------------------registro de la organizacion social------------------
        nueva_organizacion=Organizacion.objects.create(ci_estudiante=nuevo_estudiante, organizacion_matriz=postulante.organizacion_matriz,
                                                       organizacion_departamental=postulante.organizacion_departamental,organizacion_regional=postulante.organizacion_regional,
                                                       comunidad_sindicato=postulante.organizacion_comunidad,otros=postulante.comunidad_apoyo)
        if nueva_organizacion:
            respuesta['Organizacion social']="Se registro los datos de la organizacion correctamente"
    except:
        respuesta['estudiante']='No se encontro el Ci ingresado o ya se registro anteriormente'
        return Response(respuesta,status=status.HTTP_400_BAD_REQUEST)
    #----------------------------registro de los datos de los documentos presentados------------
    try:       
        postulante_documentacion=PostulantePrepaDocumentacion.objects.get(ci_postulante=ci_postulante)
        nueva_documentacion_estudiante=DocumentacionEstudiante.objects.create(ci_estudiante=nuevo_estudiante,carta_postulacion=postulante_documentacion.carta_postulacion,
                                                                              fot_diploma=postulante_documentacion.fotocopia_diploma,fot_ci=postulante_documentacion.fotocopia_ci,
                                                                              fot_certificado_nacimiento=postulante_documentacion.certificado_nacimiento,
                                                                              fotografia=postulante_documentacion.fotografias,fot_apoderados=postulante_documentacion.fotocopias_apoderados,
                                                                              carta_auspicio=postulante_documentacion.carta_auspicio,certificacion_orga=postulante_documentacion.certificacion_pertenencia,
                                                                              carta_compromiso=postulante_documentacion.carta_compromiso,formulario_ministerio=postulante_documentacion.formulario_ministerio,
                                                                              libreta_servicio_militar=postulante_documentacion.libreta_servicio_militar,observacion=postulante_documentacion.observacion,
                                                                              boleta_pago=postulante_documentacion.boleta_pago,no_pertenece_unibol=postulante_documentacion.no_pertenece_unibol)
        if nueva_documentacion_estudiante:
            respuesta['Documentacion']="la documentacion se registro correctamente"
        
    except:
        respuesta['Documentacion']="error al registrar la documentacion de estudiante"
    #------------------------------registro de los datos del apoderado del estudiante---------------------------
    try:
        postulante_apoderado=PostulantePrepaApoderado.objects.get(ci_postulante=ci_postulante)
        nuevo_responsable=ResponsableEstudiante.objects.create(ci_estudiante=nuevo_estudiante,nombre=postulante_apoderado.nom_apo1,apellidoP=postulante_apoderado.ape_apo1,
                                                               ci=postulante_apoderado.ci_apo1,celular=postulante_apoderado.telefono_apo1,ocupacion=postulante_apoderado.ocupacion_apo1,
                                                               idioma=postulante_apoderado.idioma_apo1,relacion_responsable=postulante_apoderado.parentesco1)

        if nuevo_responsable:
            respuesta['Apoderado']="La informacion del apoderado se registro Correctamente"     
            
    except:
        respuesta['Apoderado']="error al registrar los datos del apoderado"
    #------------------------------registro de los datos academicos del estudiante----------------------------------------
    try:
        postulante_academicos=PostulantePrepaDatosAcademicos.objects.get(ci_postulante=ci_postulante)
        nuevo_dato=EducacionPrimaria.objects.create(ci_estudiante=nuevo_estudiante,unidad_educativa=postulante_academicos.unidad_educativa,
                                                    anio_egreso=postulante_academicos.gestion_egreso,tipo_colegio=postulante_academicos.tipo_unidad_educativa,
                                                    departamento=postulante_academicos.departamento, provincia=postulante_academicos.provincia,estado='habilitado')
        if nuevo_dato:
            respuesta['datos secundaria']="Los datos academicos del estudiante se registraron correctamente"
    except:
        respuesta['datos secundaria']="error al intentar registrar los datos academicos secundaria"
    
    return Response(respuesta)

def ObtenerCodigoCarrera(carrera):
    if carrera=='INGENIERIA EN AGROFORESTERIA COMUNITARIA ECOLOGICA':
        return Carrera.objects.get(codigo_carrera='AGRF')
    if carrera=='INGENIERIA EN TRANSFORMACION DE ALIMENTOS':
        return Carrera.objects.get(codigo_carrera='TIAL')
    if carrera=='ECONOMIA COMUNITARIA PRODUCTIVA':
        return Carrera.objects.get(codigo_carrera='ECOP')
    if carrera=='INGENIERIA EN ACUICULTURA COMUNITARIA Y GESTION DE AGUA':
        return Carrera.objects.get(codigo_carrera='ACUC')

def ObtenerNumeroRegistro():
    ultimo_numero_registro=ControlNumeroRegistro.objects.last()
    if ultimo_numero_registro:
        ultimo_numero_registro.numero_registro+=1
        ultimo_numero_registro.save()
        return ultimo_numero_registro.numero_registro
    else:
        nuevo=ControlNumeroRegistro.objects.create(numero_registro=1,gestion=str(datetime.now().year))
        return nuevo.numero_registro
    
def obtenerUltimoNumeroRegistrado(codigo_carrera):
    print("------------",codigo_carrera)
    if codigo_carrera=='ACUC':
        ultimo_estudiante = Estudiante.objects.filter(codigo_carrera=codigo_carrera).exclude(numero_archivo__in=[370, 495]).aggregate(max_numero_archivo=Max('numero_archivo'))['max_numero_archivo']
        print("------------",ultimo_estudiante)
        return ultimo_estudiante+1
    else:
        ultimo_estudiante=Estudiante.objects.filter(codigo_carrera=codigo_carrera).aggregate(max_numero_archivo=Max('numero_archivo'))['max_numero_archivo'] 
        print("------------",ultimo_estudiante)
        return ultimo_estudiante+1    

@api_view(['DELETE']) 
def EliminarDatos(request,ci_estudiante):
    AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante).delete()
    EducacionPrimaria.objects.filter(ci_estudiante=ci_estudiante).delete()
    DocumentacionEstudiante.objects.filter(ci_estudiante=ci_estudiante).delete()
    Organizacion.objects.filter(ci_estudiante=ci_estudiante).delete()
    ResponsableEstudiante.objects.filter(ci_estudiante=ci_estudiante).delete()
    Estudiante.objects.filter(ci_estudiante=ci_estudiante).delete()
    return Response({"message":"los datos se eliminarion correctamente"},status=status.HTTP_200_OK)


@api_view(['GET'])
def InscribirEstudiantePrimerAnio(request,ci_estudiante):
    try:
        estudiante=Estudiante.objects.get(ci_estudiante=ci_estudiante)        
        ultimo_año=str(datetime.now().year)
        if estudiante.anio_ingreso==ultimo_año and estudiante.inscrito_gestion=='no':
            if estudiante.codigo_carrera.codigo_carrera=='AGRF': 
               lista_asignaturas_malla=[35,36,37,38,39,40,41,42]            
               return RegistrarMateriasPrimerAnio(estudiante,lista_asignaturas_malla)              
            
            if estudiante.codigo_carrera.codigo_carrera=='TIAL':
               lista_asignaturas_malla=[69,70,71,72,73,74,75,76]            
               return RegistrarMateriasPrimerAnio(estudiante,lista_asignaturas_malla)                             

            if estudiante.codigo_carrera.codigo_carrera=='ECOP':
               lista_asignaturas_malla=[1,2,3,4,5,6,7,8]            
               return RegistrarMateriasPrimerAnio(estudiante,lista_asignaturas_malla)               


            if estudiante.codigo_carrera.codigo_carrera=='ACUC':
               lista_asignaturas_malla=[103,104,105,106,107,108,109,110]            
               return RegistrarMateriasPrimerAnio(estudiante,lista_asignaturas_malla)                               

        else:
            return Response({"message":"el estudiante no se encuentra en el primer año o ya esta inscrito"})
    except:
        return Response({"message":"no existe el estudiante"})
    
    # return Response({"estudiante": estudiante_serializer,
    #                              "asignaturas_inscritas":asignaturas_malla_serializer,
    #                              "fecha_emision":fecha_emision,
    #                              "numero_boleta":numero_boleta,})

def RegistrarMateriasPrimerAnio(estudiante,lista_asignaturas_malla):
    for asignatura_malla in lista_asignaturas_malla:
        #estudiante=Estudiante.objects.get(ci_estudiante=ci_estudiante)
        nueva_asignatura_cursada = AsignaturaCursada.objects.create(
            ci_estudiante=estudiante,
            codigo_asignatura=MallaAcademica.objects.filter(id=asignatura_malla).first().codigo_asignatura.codigo_asignatura,
            id_malla_academica=MallaAcademica.objects.filter(id=asignatura_malla).first(),
            anio_cursado=datetime.now().year,
            estado_gestion_quechua='QHIPAKUN',
            estado_gestion_espaniol='ABANDONO',
            fecha_inscripcion=datetime.now(),
            estado_inscripcion='inscrito',
            malla_aplicada='2023',
            homologacion='NO',
            cod_carrera=estudiante.codigo_carrera.codigo_carrera
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
            nivel_carrera=VerificarGrado(estudiante.ci_estudiante)
            )                     

        if nueva_asignatura_cursada and nueva_nota:
            nueva_asignatura_cursada.id_nota=nueva_nota
            nueva_asignatura_cursada.save()
        else:
            return Response({"message":"Hubo un error al intentar registrar materias consulte con soporte"})
    lista_asignaturas=MallaAcademica.objects.filter(id__in=lista_asignaturas_malla)
    asignaturas_malla_serializer=MallaAcademicaInscripcionSerializer(lista_asignaturas,many=True).data
    numero_boleta=GenerarNuevaBoleta(estudiante.ci_estudiante)
    estudiante.inscrito_gestion='si'
    estudiante.save()
    estudiante_serializer=EstudianteInscripcionSerializer(estudiante).data
    fecha_emision=datetime.now().date()
    numero_archivo=obtenerNumeroArchivo(estudiante.ci_estudiante)
    return Response({"estudiante": estudiante_serializer,
                                 "asignaturas_inscritas":asignaturas_malla_serializer,
                                 "fecha_emision":fecha_emision,
                                 "numero_boleta":numero_boleta,
                                 'numero_archivo':numero_archivo})

def obtenerNumeroArchivo(ci_estudiante):
    estudiante=Estudiante.objects.get(ci_estudiante=ci_estudiante)
    return estudiante.numero_archivo


@api_view(['GET']) 
def reimprimirInscripcion(request,ci_estudiante):
    
    ultimo_año=str(datetime.now().year)
    anio_aterior=str(datetime.now().year-1)
    fecha_emision=datetime.now().date()
    numero_archivo=obtenerNumeroArchivo(ci_estudiante)
    estudiante=Estudiante.objects.get(ci_estudiante=ci_estudiante)
    numero_boleto=BoletaInscripcion.objects.filter(ci_estudiante=ci_estudiante).first()
    asignaturas_cursadas=AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante,anio_cursado=ultimo_año)
    asignaturas_cursadas_serializer=AsignaturasCursadasSerializerReImpresion(asignaturas_cursadas,many=True).data

    lista_asignaturas_anio_anterior=AsignaturaCursada.objects.filter(anio_cursado=anio_aterior,ci_estudiante=ci_estudiante).order_by('codigo_asignatura')
    lista_asignaturas_anio_anterior_serializer=AsignaturaCursadaAnioAnteriorSerializer(lista_asignaturas_anio_anterior,many=True).data
    

    estudiante_serializer=EstudianteInscripcionSerializer(estudiante).data
    
    if estudiante:
        return Response({"estudiantes": estudiante_serializer,
                         "asignaturas_tomadas":asignaturas_cursadas_serializer,
                         "asignaturas_anio_anterior":lista_asignaturas_anio_anterior_serializer,
                         "anio_actual":ultimo_año,
                         "numero_boleta":numero_boleto.numero_boleta,
                         "numero_archivo":numero_archivo,
                         "fecha_emision":fecha_emision})       
    else:
        return Response({"message":"error al optener los estudantes"},status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET']) 
def cancelarInscripcion(request, ci_estudiante):
    try:
        # Verificar si el estudiante existe
        estudiante = Estudiante.objects.get(ci_estudiante=ci_estudiante)
    except ObjectDoesNotExist:
        return Response({"message": "No se encontró el estudiante."}, status=status.HTTP_404_NOT_FOUND)
    
    # Obtener el año actual como cadena
    ultimo_año = str(datetime.now().year)
    
    # Eliminar las notas de estudiante para las asignaturas cursadas en el año actual
    asignaturas_cursadas = AsignaturaCursada.objects.filter(ci_estudiante=ci_estudiante, anio_cursado=ultimo_año)
    notas_eliminadas = NotaEstudiante.objects.filter(id_asignatura_cursada__in=asignaturas_cursadas)
    
    # Eliminar las asignaturas cursadas para el año actual
    asignaturas_cursadas.delete()
    notas_eliminadas.delete()
    # Actualizar el estado de inscripción del estudiante
    estudiante.inscrito_gestion = 'no'
    estudiante.save()
    
    
    # Mensaje de respuesta detallado
    response_message = {
        "message": "La inscripción del estudiante se canceló correctamente." }
    
    return Response(response_message, status=status.HTTP_200_OK)
