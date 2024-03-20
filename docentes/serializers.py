from rest_framework import serializers
from parametros.models import Docente


class DocenteSerializer(serializers.ModelSerializer):
    nombre_asignatura=serializers.SerializerMethodField()
    anio_asignado=serializers.SerializerMethodField()
    codigo_carrera=serializers.SerializerMethodField()

    class Meta:
        model = Docente
        fields = ('nombres','apellidop','apellidop','ci','celular','profesion','created','correo','numero_item','id_asignatura','nombre_asignatura','anio_asignado','codigo_carrera','estado')

    def get_nombre_asignatura(self,docente):
        asignatura=docente.id_asignatura
        return asignatura.nombre_asignatura if asignatura else None
    def get_anio_asignado(self,docente):
        asignatura=docente.id_asignatura
        return asignatura.anio_asignado if asignatura else None
    def get_codigo_carrera(self,docente):
        asignatura=docente.id_asignatura
        return asignatura.carrera_codigo if asignatura else None
