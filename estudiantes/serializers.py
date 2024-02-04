from rest_framework import serializers
from parametros.models import*

class EstudianteSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields =('ci_estudiante','nombres','apellidoP','apellidoM','celular','nombre_carrera','anio_ingreso','anio_cursado','obs1','obs2','obs3','inscrito_gestion','estado')
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
        fields = ('ci_estudiante','codigo_asignatura','anio_cursado','estado_gestion_espaniol','nota_num_final','nombre_asignatura','total_horas','pre_requisitos')

    def get_nota_num_final(self, asignatura):
        nota =asignatura.id_nota
        return nota.nota_num_final if nota else None
    def get_nombre_asignatura(self, asignatura_cursada):
        malla=asignatura_cursada.id_malla_academica
        return malla.codigo_asignatura.nombre_asignatura if malla else None
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

