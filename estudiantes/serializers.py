from rest_framework import serializers
from parametros.models import*

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

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
