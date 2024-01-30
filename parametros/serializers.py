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
        fields = '__all__'

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
    class Meta:
        model = Asignatura
        fields = '__all__'