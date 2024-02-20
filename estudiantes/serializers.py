from rest_framework import serializers
from parametros.models import*

class EstudianteSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields =('ci_estudiante','ci_especial','apellidoP','apellidoM','nombres','nombre_carrera','tipo_ingreso','anio_ingreso','numero_archivo','anio_cursado','obs1','obs2','estado','inscrito_gestion')
    def get_nombre_carrera(self, estudiante):
        carrera=estudiante.codigo_carrera
        return carrera.nombre_carrera if carrera else None    
    

class DocumentacionEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentacionEstudiante
        fields = '__all__'

class OrganizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizacion
        fields = '__all__'

class ResponsableEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponsableEstudiante
        fields = '__all__'

class EducacionPrimariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducacionPrimaria
        fields = '__all__'

class AsignaturaCursadaSerializer(serializers.ModelSerializer):
    nota_num_final=serializers.SerializerMethodField()
    nombre_asignatura=serializers.SerializerMethodField()
    total_horas=serializers.SerializerMethodField()
    pre_requisitos=serializers.SerializerMethodField()
    class Meta:
        model = AsignaturaCursada
        fields = ('ci_estudiante','codigo_asignatura','convalidacion','homologacion','anio_cursado','estado_gestion_espaniol','nota_num_final','nombre_asignatura','total_horas','pre_requisitos')

    def get_nota_num_final(self, asignatura):
        nota =asignatura.id_nota
        return nota.nota_num_final if nota else None
    def get_nombre_asignatura(self, asignatura_cursada):
        if asignatura_cursada.codigo_asignatura=='LCEC 404' and asignatura_cursada.anio_cursado=='2022':
            asignatura_cursada.codigo_asignatura='LCEC 406'
            asignatura_cursada.save()
        if asignatura_cursada.codigo_asignatura=='LCEC 408'and asignatura_cursada.anio_cursado=='2022':
            asignatura_cursada.codigo_asignatura='LCEC 402'
            asignatura_cursada.save()
            
        malla=asignatura_cursada.id_malla_academica
        if asignatura_cursada.malla_aplicada=='2018' and asignatura_cursada.homologacion=='NO':
            return malla.codigo_asignatura.asignatura_malla_2018 if malla else None
        elif asignatura_cursada.malla_aplicada=='2018' and asignatura_cursada.homologacion=='SI' and asignatura_cursada.convalidacion!='':
            #malla2018=MallaAcademica2018.objects.filter(codigo=asignatura_cursada.convalidacion).first()
            #return malla2018.asignatura if malla2018 else None
            asignatura=Asignatura.objects.get(codigo_asignatura=asignatura_cursada.convalidacion)
            return asignatura.nombre_asignatura if asignatura else None
        elif asignatura_cursada.malla_aplicada=='2018' and asignatura_cursada.homologacion=='SI' and asignatura_cursada.codigo_asignatura=='LCEC 402':
                return 'MONITOREO Y EVALUACIÓN DEL SISTEMA PRODUCTIVO'
        elif asignatura_cursada.malla_aplicada=='2018' and asignatura_cursada.homologacion=='SI' and asignatura_cursada.codigo_asignatura=='LCEC 406':
                return 'MERCADEO Y COMERCIALIZACIÓN '
        else:
            return malla.codigo_asignatura.nombre_asignatura if malla else None
 #MONITOREO Y EVALUACIÓN DEL SISTEMA PRODUCTIVO
 #MERCADEO Y COMERCIALIZACIÓN                  
    def get_total_horas(self,asignatura_cursada):
        malla=asignatura_cursada.id_malla_academica
        return malla.codigo_asignatura.total_horas if malla else None
    def get_pre_requisitos(self,asignatura_cursada):
        malla=asignatura_cursada.id_malla_academica
        if malla.codigo_asignatura.pre_requisito2:
            requisitos=malla.codigo_asignatura.pre_requisito1+(","+malla.codigo_asignatura.pre_requisito2)
        else:
            requisitos=malla.codigo_asignatura.pre_requisito1
        return requisitos if malla else None
    

class NotaEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaEstudiante
        fields = '__all__'

class EstudianteHistorialSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    class Meta:
        model =Estudiante
        fields =('ci_estudiante','nombres','apellidoP','apellidoM','numero_registro','nombre_carrera')
    def get_nombre_carrera(self,estudiante):
        carrera=estudiante.codigo_carrera
        return carrera.nombre_carrera if carrera else None

class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = '__all__'

class MallaAcademicaSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    nombre_asignatura=serializers.SerializerMethodField()
    class Meta:
        model = MallaAcademica
        fields = '__all__'
    def get_nombre_carrera(self,malla):
        carrera=malla.codigo_carrera
        return carrera.nombre_carrera if carrera else None
    def get_nombre_asignatura(self,malla):
         asignatura = malla.codigo_asignatura
         return asignatura.nombre_asignatura if asignatura else None


class AsignaturaCursadaNotaSerializer(serializers.ModelSerializer):
    nota_num_gestion=serializers.SerializerMethodField()
    instancia=serializers.SerializerMethodField()
    nota_num_instancia=serializers.SerializerMethodField()
    nota_num_final=serializers.SerializerMethodField()
    nota_literal_quechua=serializers.SerializerMethodField()
    resultado_gestion=serializers.SerializerMethodField()    
    resultado_gestion_espaniol=serializers.SerializerMethodField()

    class Meta:
        model = AsignaturaCursada
        fields = ('codigo_asignatura','anio_cursado','estado_gestion_quechua','estado_gestion_espaniol','nota_num_gestion','instancia','nota_num_instancia','nota_num_final','nota_literal_quechua','resultado_gestion','')