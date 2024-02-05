from rest_framework import serializers
from parametros.models import*

# class EstudianteSerializer(serializers.ModelSerializer):
#     nombre_carrera=serializers.SerializerMethodField()
#     class Meta:
#         model = Estudiante
#         fields = '__all__'
#     def get_nombre_carrera(self, estudiante):
#         carrera=estudiante.codigo_carrera
#         return carrera.nombre_carrera if carrera else None
class EstudianteSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields = '__all__'
    def get_nombre_carrera(self, estudiante):
        carrera=estudiante.codigo_carrera
        return carrera.nombre_carrera if carrera else None
       
class EstudianteInscripcionSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    class Meta:
        model =Estudiante
        fields=('ci_estudiante','nombres','apellidoP','apellidoM','codigo_carrera','nombre_carrera','anio_cursado','inscrito_gestion')
    def get_nombre_carrera(self, estudiante):
        carrera=estudiante.codigo_carrera
        return carrera.nombre_carrera if carrera else None

class MallaAcademicaInscripcionSerializer(serializers.ModelSerializer):
    nombre_asignatura=serializers.SerializerMethodField()
    anio_asignado=serializers.SerializerMethodField()
    class Meta:
        model = MallaAcademica
        fields =('id','codigo_carrera','codigo_asignatura','nombre_asignatura','anio_asignado')

    def get_nombre_asignatura(self,malla):
         asignatura = malla.codigo_asignatura
         return asignatura.nombre_asignatura if asignatura else None
    def get_anio_asignado(self,malla):
        asignatura=malla.codigo_asignatura
        return asignatura.anio_asignado if asignatura else None