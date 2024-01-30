from rest_framework import serializers
from parametros.models import*

class EstudianteSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields = '__all__'
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
    class Meta:
        model = AsignaturaCursada
        fields = '__all__'

class NotaEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaEstudiante
        fields = '__all__'


class MallaAcademicaSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    #nombre_asignatura=serializers.SerializerMethodField()
    class Meta:
        model = MallaAcademica
        fields = '__all__'
    def get_nombre_carrera(self,malla):
        carrera=malla.codigo_carrera
        return carrera.nombre_carrera if carrera else None
    # def get_nombre_asignatura(self,malla):
    #      asignatura = malla.codigo_asignatura
    #      return asignatura if asignatura else None