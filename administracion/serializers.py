from rest_framework import serializers
from parametros.models import*
from django.contrib.auth.models import User,Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass
class EmptySerializer(serializers.Serializer):
    pass
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model =User
        fields=('username','email','first_name','last_name')

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
    numero_boleta=serializers.SerializerMethodField()
    class Meta:
        model =Estudiante
        fields=('ci_estudiante','nombres','apellidoP','apellidoM','codigo_carrera','nombre_carrera','numero_registro','anio_cursado','inscrito_gestion','anio_ingreso','tipo_ingreso','numero_boleta','ci_especial')
    def get_nombre_carrera(self, estudiante):
        carrera=estudiante.codigo_carrera
        return carrera.nombre_carrera if carrera else None
    def get_numero_boleta(self, estudiante):
        ci=estudiante.ci_estudiante
        boleta=BoletaInscripcion.objects.filter(ci_estudiante=ci).first()
        return boleta.numero_boleta if boleta else None

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
    

class PostulantePrepaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostulantePrepa
        fields =('ci_postulante','nombres_p','apellido_paterno_p','apellido_materno_p','anio_postulacion','nota_final','carrera','estado_ingreso','registrado')
   


class AsignaturaCursadaAnioAnteriorSerializer(serializers.ModelSerializer):
    nombre_asignatura=serializers.SerializerMethodField()
    nota_num_final=serializers.SerializerMethodField()
    observacion=serializers.SerializerMethodField()
    class Meta:
        model = AsignaturaCursada
        fields=('codigo_asignatura','nombre_asignatura','nota_num_final','estado_gestion_espaniol','observacion')

    def get_nombre_asignatura(self,asignatura_cursada):
         malla = asignatura_cursada.id_malla_academica
         return malla.codigo_asignatura.nombre_asignatura if malla else None
    def get_nota_num_final(self, asignatura_cursada):
        nota =asignatura_cursada.id_nota
        return nota.nota_num_final if nota else None
    def get_observacion(self,asignatura_cursada):
        malla=asignatura_cursada.id_malla_academica
        return malla.codigo_asignatura.detalle if malla else None
    #fffffffffffffffffffffffffffffaaaaaaaaaaaaaaaaaaaaaallllllllllllllllllta es para las boletas

class AsignaturasCursadasSerializerReImpresion(serializers.ModelSerializer):
    nombre_asignatura=serializers.SerializerMethodField()
    tipo=serializers.SerializerMethodField()
    observacion=serializers.SerializerMethodField()
    class Meta:
        model = AsignaturaCursada
        fields=('codigo_asignatura','nombre_asignatura','tipo','observacion')

    def get_nombre_asignatura(self,asignatura_cursada):
         malla = asignatura_cursada.id_malla_academica
         return malla.codigo_asignatura.nombre_asignatura if malla else None
    def get_tipo(self,asignatura_cursada):
         malla = asignatura_cursada.id_malla_academica
         return malla.codigo_asignatura.tipo if malla else None
    def get_observacion(self,asignatura_cursada):
         malla = asignatura_cursada.id_malla_academica
         return None
