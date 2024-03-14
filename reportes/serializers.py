from rest_framework import serializers
from parametros.models import*


class EstudianteCarreraAnioSerializer(serializers.ModelSerializer):
    nombre_carrera=serializers.SerializerMethodField()
    ci=serializers.SerializerMethodField()
    class Meta:
        model = Estudiante
        fields =('apellidoP','apellidoM','nombres','ci')
    def get_nombre_carrera(self, estudiante):
        carrera=estudiante.codigo_carrera
        return carrera.nombre_carrera if carrera else None 
    def get_ci(self, estudiante):
        ci_completo=str(estudiante.ci_estudiante)+" "+str(estudiante.ci_especial)
        return ci_completo if ci_completo else None   
    