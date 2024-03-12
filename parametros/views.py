from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class AsignaturaView(viewsets.ModelViewSet):
    queryset=Asignatura.objects.all()
    serializer_class=AsignaturaSerializer
    
@permission_classes([IsAuthenticated])    
class CarreraView(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()    
    serializer_class = CarreraSerializer

class MunicipioView(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()    
    serializer_class = MunicipioSerializer

class ProvinciaView(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()    
    serializer_class = ProvinciaSerializer

class DepartamentoView(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()    
    serializer_class = DepartamentoSerializer

class IdiomaOriginarioView(viewsets.ModelViewSet):
    queryset = IdiomaOriginario.objects.all()    
    serializer_class = IdiomaOriginarioSerializer

class AnioCarreraView(viewsets.ModelViewSet):
    queryset = AnioCarrera.objects.all()    
    serializer_class = AnioCarreraSerializer

class NumerosLetrasView(viewsets.ModelViewSet):
    queryset = NumerosLetras.objects.all() 
    serializer_class = NumerosLetrasSerializer
@api_view(['GET'])
def ObtenerMallaPorCarrera(request,codigo_carrera):
    queryset=MallaAcademica.objects.filter(codigo_carrera=codigo_carrera)
    serializer_class=MallaAcademicaSerializer(queryset,many=True).data
    return Response(serializer_class)
#@api_view(['GET']) 
# def actualizar_tablas(request):
#     #=========================================CARGADO DE DATOS DEL ESTUDIANTE, NOTAS, Y OTRAS TABLAS DE BASE ANTERIOR=========================
#      estudiante2=Estudiante2.objects.all()
#      for e in estudiante2:
#           ci_estudiante=int(e.ci_estudiante)
#           ext=e.ext
#           apellidop=e.apellidop
#           apellidom=e.apellidom
#           nombres=e.nombres
#           telefono=e.telefono
#           codigoc=e.codigoc
#           carrera=e.carrera
#           gestion=e.gestion
#           genero=e.genero
#           tipoingreso=e.tipoingreso
#           archivo=e.archivo
#           registro=e.registro
#           fecha_nacimiento=e.fecha_nacimiento
#           dep_nacimiento=e.dep_nacimiento
#           prov_naci=e.prov_naci
#           munic_nac=e.munic_nac
#           email=e.email
#           obs1=e.nacionalidad
#           if obs1=='RETIRADO':
#               estado='inhabilitado'
#           else:
#               estado='habilitado'
#           obs2=e.observado
#           obs3=e.observado2023

#           convalidacion=e.convalidacion
#           titulacion=e.titulacion
#           homologacion=e.homologacion
#           anio_cursado=e.estadocivil
#           estado_convalidacion=e.estado_convalidacion
#           carrera_nueva=Carrera.objects.get(nombre_carrera=carrera)
#           fecha_nacimiento_formateado=datetime.strptime(fecha_nacimiento,"%d/%m/%Y").date()

#           estudiante=Estudiante.objects.create(ci_estudiante=ci_estudiante,extencion=ext,codigo_carrera=carrera_nueva,nombres=nombres,apellidoP=apellidop,
#                                     apellidoM=apellidom,celular=telefono,genero=genero,fecha_nacimiento=fecha_nacimiento_formateado,depa_nacimiento=dep_nacimiento,
#                                     prov_nacimiento=prov_naci,munic_nacimiento=munic_nac,tipo_ingreso=tipoingreso,email=email,
#                                     anio_ingreso=gestion, numero_archivo=archivo, homologacion=homologacion,convalidacion=convalidacion,titulado=titulacion,
#                                     numero_registro=registro, anio_cursado=anio_cursado,estado_convalidacion=estado_convalidacion,
#                                     obs1=obs1,obs2=obs2,obs3=obs3,inscrito_gestion='no',estado=estado,baja='no')

#           org_matriz=e.org_matriz
#           org_regional=e.org_regional
#           org_comunidad=e.org_comunidad
#           Organizacion.objects.create(ci_estudiante=estudiante,organizacion_matriz=org_matriz,organizacion_regional=org_regional,comunidad_sindicato=org_comunidad)
#         #----------------------------------------------------------------------------------------------------------------------------------------------------------------
#           notas=NotaEstudiante2.objects.filter(cod_estudiante=estudiante.ci_estudiante)
#           for nota in notas:
#             cod_estudiante=nota.cod_estudiante
#             gestion_cursada=nota.gestionnota
#             estado_gestion_quechua=nota.resultado_gestion
#             estado_gestion_espaniol=nota.estado_calificacion
#             codigo_asignaturaa=nota.cod_asignatura
#             codigo_carrera=nota.codigoc

#             convalidacion=nota.convalidacion
#             malla_aplicada=nota.malla_aplicada
#             homologacion=nota.homologacion
#             codigo_malla_ajustada=nota.codigo_malla_ajustada
#             cod_carrera=nota.codigoc



#             try:
#                 malla_academica=MallaAcademica.objects.get(codigo_carrera=codigo_carrera,codigo_asignatura=codigo_asignaturaa)
#                 #print("QQQQQQQQQQQQQQ",malla_academica)
#                 #if malla_aplicada=='2023':
#                 asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,id_malla_academica=malla_academica,codigo_asignatura= codigo_asignaturaa,
#                                                                 anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
#                                                                 estado_inscripcion="concluido",convalidacion=convalidacion,malla_aplicada=malla_aplicada,homologacion=homologacion,
#                                                                 codigo_malla_ajustada=codigo_malla_ajustada,cod_carrera=cod_carrera)
#                 # else:
#                 #     asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,codigo_asignatura= codigo_asignaturaa,
#                 #                                                 anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
#                 #                                                 estado_inscripcion="concluido",convalidacion=convalidacion,malla_aplicada=malla_aplicada,homologacion=homologacion,
#                 #                                                 codigo_malla_ajustada=codigo_malla_ajustada,cod_carrera=cod_carrera)
#             except:
#                 asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,codigo_asignatura= codigo_asignaturaa,
#                                                                 anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
#                                                                 estado_inscripcion="concluido")

#             nota_gestion=nota.nota_gestion
#             instancia="no"
#             nota_instancia=nota.instancia
#             if nota_instancia:
#                 instancia="si"
#                 nota_instancia=int(nota.instancia)
#             nota_final=nota.nota_final
#             nota_quechua=nota.nota_quechua
#             res_cualitativo=nota.res_cualitativo
#             resultado_gestion=nota.resultado_gestion
#             nivel_carrera=nota.nivel
#             notas_actual=NotaEstudiante.objects.create(id_asignatura_cursada=asignaturaCursada.id,nota_num_gestion=nota_gestion,instancia=instancia,
#                                                 nota_num_instancia=nota_instancia,nota_num_final=nota_final,nota_literal_quechua=nota_quechua,
#                                                 res_cualitativo=res_cualitativo,resultado_gestion=resultado_gestion,gestion_cursada=gestion_cursada,
#                                                 resultado_gestion_espaniol=estado_gestion_espaniol,nivel_carrera=nivel_carrera)
#             asignaturaCursada.id_nota=notas_actual
#             asignaturaCursada.save()
    #=============================================================================================================

     

     #=======================CARGADO DE NOTAS DE ESTUDIANTES ESPECIFICOS==========================================
@api_view(['GET']) 
def actualizarNotaEstudianteEspecial(request):
     notas=NotaEstudiante2.objects.filter(cod_estudiante='6719461-1O')
     if not notas:
         return Response({"message":"no se encontro registros"})
     for nota in notas:
            cod_estudiante=nota.cod_estudiante
            gestion_cursada=nota.gestionnota
            estado_gestion_quechua=nota.resultado_gestion
            codigo_asignaturaa=nota.cod_asignatura
            codigo_carrera=nota.codigoc
            estado_gestion_espaniol=nota.estado_calificacion
            convalidacion=nota.convalidacion
            malla_aplicada=nota.malla_aplicada
            homologacion=nota.homologacion
            codigo_malla_ajustada=nota.codigo_malla_ajustada
            cod_carrera=nota.codigoc
            estudiante=Estudiante.objects.get(ci_estudiante=6719461)
            try:
                malla_academica=MallaAcademica.objects.get(codigo_carrera=codigo_carrera,codigo_asignatura=codigo_asignaturaa)
                print("QQQQQQQQQQQQQQ",malla_academica)
                asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,id_malla_academica=malla_academica,codigo_asignatura= codigo_asignaturaa,
                                                                anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,
                                                                estado_inscripcion="concluido",estado_gestion_espaniol=estado_gestion_espaniol,convalidacion=convalidacion,
                                                                malla_aplicada=malla_aplicada,homologacion=homologacion,
                                                                codigo_malla_ajustada=codigo_malla_ajustada,cod_carrera=cod_carrera)
            except:
                asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,codigo_asignatura= codigo_asignaturaa,
                                                                anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
                                                                estado_inscripcion="concluido")

            nota_gestion=nota.nota_gestion
            instancia="no"
            nota_instancia=nota.instancia
            if nota_instancia:
                instancia="si"
                nota_instancia=int(nota.instancia)
            nota_final=nota.nota_final
            nota_quechua=nota.nota_quechua
            res_cualitativo=nota.res_cualitativo
            resultado_gestion=nota.resultado_gestion
            nivel_carrera=nota.nivel
            notas_actual=NotaEstudiante.objects.create(id_asignatura_cursada=asignaturaCursada.id,nota_num_gestion=nota_gestion,instancia=instancia,
                                                nota_num_instancia=nota_instancia,nota_num_final=nota_final,nota_literal_quechua=nota_quechua,
                                                res_cualitativo=res_cualitativo,resultado_gestion=resultado_gestion,gestion_cursada=gestion_cursada,
                                                resultado_gestion_espaniol=estado_gestion_espaniol,nivel_carrera=nivel_carrera)
            
            asignaturaCursada.id_nota=notas_actual
            asignaturaCursada.save()
    #==============================================================================================================================
     return Response({"respuesta":"Respuesta exitosa "})

@api_view(['GET']) 
def ObtenerProvincias(request,nombre_departamento):
    lista_provincias=Provincia.objects.filter(id_departamento__nombre_departamento=nombre_departamento)
    serializer_lista_provincias=ProvinciaSerializer(lista_provincias,many=True).data
    return Response(serializer_lista_provincias)

