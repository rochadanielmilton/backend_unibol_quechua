from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from datetime import datetime


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
def actualizar_tablas(request):
    #=========================================CARDO DE DATOS DEL ESTUDIANTE, NOTAS, Y OTRAS TABLAS=========================
    #  estudiante2=Estudiante2.objects.all()
    #  for e in estudiante2:
    #       ci_estudiante=int(e.ci_estudiante)
    #       ext=e.ext
    #       apellidop=e.apellidop
    #       apellidom=e.apellidom
    #       nombres=e.nombres
    #       telefono=e.telefono
    #       codigoc=e.codigoc
    #       gestion=e.gestion
    #       genero=e.genero
    #       tipoingreso=e.tipoingreso
    #       archivo=e.archivo
    #       registro=e.registro
    #       fecha_nacimiento=e.fecha_nacimiento
    #       dep_nacimiento=e.dep_nacimiento
    #       prov_naci=e.prov_naci
    #       munic_nac=e.munic_nac
    #       email=e.email
    #       obs1=e.nacionalidad
    #       obs2=e.observado
    #       obs3=e.observado2023
    #       estado=e.estado
    #       convalidacion=e.convalidacion
    #       titulacion=e.titulacion
    #       homologacion=e.homologacion
    #       anio_cursado=e.estadocivil
    #       estado_convalidacion=e.estado_convalidacion
    #       carrera_nueva=Carrera.objects.get(codigo_carrera=codigoc)
    #       fecha_nacimiento_formateado=datetime.strptime(fecha_nacimiento,"%d/%m/%Y").date()

    #       estudiante=Estudiante.objects.create(ci_estudiante=ci_estudiante,extencion=ext,codigo_carrera=carrera_nueva,nombres=nombres,apellidoP=apellidop,
    #                                 apellidoM=apellidom,celular=telefono,genero=genero,fecha_nacimiento=fecha_nacimiento_formateado,depa_nacimiento=dep_nacimiento,
    #                                 prov_nacimiento=prov_naci,munic_nacimiento=munic_nac,tipo_ingreso=tipoingreso,email=email,
    #                                 anio_ingreso=gestion, numero_archivo=archivo, homologacion=homologacion,convalidacion=convalidacion,titulado=titulacion,
    #                                 estado=estado,numero_registro=registro, anio_cursado=anio_cursado,estado_convalidacion=estado_convalidacion,
    #                                 obs1=obs1,obs2=obs2,obs3=obs3)

    #       org_matriz=e.org_matriz
    #       org_regional=e.org_regional
    #       org_comunidad=e.org_comunidad
    #       Organizacion.objects.create(ci_estudiante=estudiante,organizacion_matriz=org_matriz,organizacion_regional=org_regional,comunidad_sindicato=org_comunidad)
    #       notas=NotaEstudiante2.objects.filter(cod_estudiante=estudiante.ci_estudiante)
    #       for nota in notas:
    #         cod_estudiante=nota.cod_estudiante
    #         gestion_cursada=nota.gestionnota
    #         estado_gestion_quechua=nota.resultado_gestion
    #         estado_gestion_espaniol=nota.estado_calificacion
    #         codigo_asignaturaa=nota.cod_asignatura
    #         codigo_carrera=nota.codigoc
    #         try:
    #             malla_academica=MallaAcademica.objects.get(codigo_carrera=codigo_carrera,codigo_asignatura=codigo_asignaturaa)
    #             print("QQQQQQQQQQQQQQ",malla_academica)
    #             asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,id_malla_academica=malla_academica,codigo_asignatura= codigo_asignaturaa,
    #                                                             anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
    #                                                             estado_inscripcion="concluido")
    #         except:
    #             asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,codigo_asignatura= codigo_asignaturaa,
    #                                                             anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
    #                                                             estado_inscripcion="concluido")

    #         nota_gestion=nota.nota_gestion
    #         instancia="no"
    #         nota_instancia=nota.instancia
    #         if nota_instancia:
    #             instancia="si"
    #             nota_instancia=int(nota.instancia)
    #         nota_final=nota.nota_final
    #         nota_quechua=nota.nota_quechua
    #         res_cualitativo=nota.res_cualitativo
    #         resultado_gestion=nota.resultado_gestion
    #         nivel_carrera=nota.nivel
    #         notas_actual=NotaEstudiante.objects.create(id_asignatura_cursada=asignaturaCursada,nota_num_gestion=nota_gestion,instancia=instancia,
    #                                             nota_num_instancia=nota_instancia,nota_num_final=nota_final,nota_literal_quechua=nota_quechua,
    #                                             res_cualitativo=res_cualitativo,resultado_gestion=resultado_gestion,gestion_cursada=gestion_cursada,
    #                                             nota_literal_espaniol=estado_gestion_espaniol,nivel_carrera=nivel_carrera)
    #=============================================================================================================

     

     #=======================CARGADO DE NOTAS DE ESTUDIANTES ESPECIFICOS==========================================
    #  notas=NotaEstudiante2.objects.filter(cod_estudiante='6719461-1O')
    #  for nota in notas:
    #         cod_estudiante=nota.cod_estudiante
    #         gestion_cursada=nota.gestionnota
    #         estado_gestion_quechua=nota.resultado_gestion
    #         estado_gestion_espaniol=nota.estado_calificacion
    #         codigo_asignaturaa=nota.cod_asignatura
    #         codigo_carrera=nota.codigoc
    #         estudiante=Estudiante.objects.get(ci_estudiante=6719461)
    #         try:
    #             malla_academica=MallaAcademica.objects.get(codigo_carrera=codigo_carrera,codigo_asignatura=codigo_asignaturaa)
    #             print("QQQQQQQQQQQQQQ",malla_academica)
    #             asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,id_malla_academica=malla_academica,codigo_asignatura= codigo_asignaturaa,
    #                                                             anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
    #                                                             estado_inscripcion="concluido")
    #         except:
    #             asignaturaCursada=AsignaturaCursada.objects.create(ci_estudiante=estudiante,codigo_asignatura= codigo_asignaturaa,
    #                                                             anio_cursado=gestion_cursada, estado_gestion_quechua=estado_gestion_quechua,estado_gestion_espaniol=estado_gestion_espaniol,
    #                                                             estado_inscripcion="concluido")

    #         nota_gestion=nota.nota_gestion
    #         instancia="no"
    #         nota_instancia=nota.instancia
    #         if nota_instancia:
    #             instancia="si"
    #             nota_instancia=int(nota.instancia)
    #         nota_final=nota.nota_final
    #         nota_quechua=nota.nota_quechua
    #         res_cualitativo=nota.res_cualitativo
    #         resultado_gestion=nota.resultado_gestion
    #         nivel_carrera=nota.nivel
    #         notas_actual=NotaEstudiante.objects.create(id_asignatura_cursada=asignaturaCursada,nota_num_gestion=nota_gestion,instancia=instancia,
    #                                             nota_num_instancia=nota_instancia,nota_num_final=nota_final,nota_literal_quechua=nota_quechua,
    #                                             res_cualitativo=res_cualitativo,resultado_gestion=resultado_gestion,gestion_cursada=gestion_cursada,
    #                                             nota_literal_espaniol=estado_gestion_espaniol,nivel_carrera=nivel_carrera)
    #==============================================================================================================================
     return Response({"respuesta":"Respuesta exitosa "})


