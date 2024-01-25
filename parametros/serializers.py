from rest_framework import serializers
from .models import *


class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignatura
        fields = '__all__'

class MallaAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MallaAcademica
        fields = '__all__'


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'