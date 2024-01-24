from rest_framework import serializers
from .models import Estudiante,Carrera


# class CarreraSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Carrera
#         fields = '__all__'


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'