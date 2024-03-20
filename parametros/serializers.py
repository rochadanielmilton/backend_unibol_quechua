from rest_framework import serializers
from .models import *

class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('id','nombre_provincia','id_departamento')

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class IdiomaOriginarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdiomaOriginario
        fields = '__all__'

class AnioCarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnioCarrera
        fields = '__all__'

class NumerosLetrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumerosLetras
        fields = '__all__'

class AsignaturaSerializer(serializers.ModelSerializer):
    nombre_docente=serializers.SerializerMethodField()
    class Meta:
        model = Asignatura
        fields = '__all__'
    def get_nombre_docente(self,asignatura):
        docente=asignatura.id_docente
        print("---------",docente)
        if docente:
            nombre_docente=docente.nombres+" "+docente.apellidop+" "+ docente.apellidom
            return nombre_docente
        else:
            return None
    
class MallaAcademicaSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    nombre_asignatura=serializers.SerializerMethodField()
    class Meta:
        model = MallaAcademica
        fields = ('id','codigo_carrera','nombre_carrera','codigo_asignatura','nombre_asignatura','descripcion','estado')
    def get_nombre_carrera(self,malla):
        carrera=malla.codigo_carrera
        return carrera.nombre_carrera if carrera else None
    def get_nombre_asignatura(self,malla):
         asignatura = malla.codigo_asignatura
         return asignatura.nombre_asignatura if asignatura else None