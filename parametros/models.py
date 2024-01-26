
from django.db import models

class AnioCarrera(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre_anio = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'anio_carrera'


class Asignatura(models.Model):
    id = models.SmallAutoField(primary_key=True)
    id_docente = models.ForeignKey('Docente', models.DO_NOTHING, db_column='id_docente', blank=True, null=True)
    codigo_asignatura = models.CharField(max_length=30, blank=True, null=True)
    nombre_asignatura = models.CharField(max_length=150, blank=True, null=True)
    descripccion = models.CharField(max_length=255, blank=True, null=True)
    horas_practicas = models.SmallIntegerField(blank=True, null=True)
    horas_teoricas = models.SmallIntegerField(blank=True, null=True)
    total_horas = models.SmallIntegerField(blank=True, null=True)
    pre_requisito1 = models.CharField(max_length=100, blank=True, null=True)
    pre_requisito2 = models.CharField(max_length=100, blank=True, null=True)
    anio_asignado = models.CharField(max_length=20, blank=True, null=True, db_comment='el a├▒o al que pertenece la materia')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asignatura'


class AsignaturaCursada(models.Model):
    id = models.SmallAutoField(primary_key=True)
    ci_estudiante = models.ForeignKey('Estudiante', models.DO_NOTHING, db_column='ci_estudiante', blank=True, null=True)
    id_asignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='id_asignatura', blank=True, null=True)
    id_malla_academica = models.ForeignKey('MallaAcademica', models.DO_NOTHING, db_column='id_malla_academica', blank=True, null=True)
    anio_cursado = models.CharField(max_length=20, blank=True, null=True)
    gestion_actual = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True, db_comment='aprobado/repro/cursando/abandonado')
    fecha_inscripcion = models.DateTimeField(blank=True, null=True)
    estado_inscripcion = models.CharField(max_length=30, blank=True, null=True, db_comment='si/concluido')
    observacion = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asignatura_cursada'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Carrera(models.Model):
    id = models.SmallAutoField(primary_key=True)
    codigo_carrera = models.CharField(max_length=30, blank=True, null=True)
    nombre_carrera = models.CharField(max_length=100, blank=True, null=True)
    documento_creacion = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrera'


class Departamento(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departamento'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Docente(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidop = models.CharField(db_column='apellidoP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellidom = models.CharField(db_column='apellidoM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ci = models.SmallIntegerField(blank=True, null=True)
    celular = models.SmallIntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    profesion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'docente'


class DocumentacionEstudiante(models.Model):
    id = models.SmallAutoField(primary_key=True)
    ci_estudiante = models.ForeignKey('Estudiante', models.DO_NOTHING, db_column='ci_estudiante', blank=True, null=True)
    carta_postulacion = models.CharField(max_length=10, blank=True, null=True)
    fot_diploma = models.CharField(max_length=10, blank=True, null=True)
    fot_ci = models.CharField(max_length=10, blank=True, null=True)
    fot_certificado_nacimiento = models.CharField(max_length=10, blank=True, null=True)
    fotografia = models.CharField(max_length=10, blank=True, null=True)
    fot_apoderados = models.CharField(max_length=10, blank=True, null=True)
    carta_auspicio = models.CharField(max_length=10, blank=True, null=True)
    certificacion_orga = models.CharField(max_length=10, blank=True, null=True)
    carta_compromiso = models.CharField(max_length=10, blank=True, null=True)
    formulario_ministerio = models.CharField(max_length=10, blank=True, null=True)
    libreta_servicio_militar = models.CharField(max_length=10, blank=True, null=True)
    boleta_pago = models.CharField(max_length=10, blank=True, null=True)
    observacion = models.CharField(max_length=10, blank=True, null=True)
    no_pertenece_unibol = models.CharField(max_length=10, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documentacion_estudiante'


class EducacionPrimaria(models.Model):
    id = models.SmallAutoField(primary_key=True)
    ci_estudiante = models.ForeignKey('Estudiante', models.DO_NOTHING, db_column='ci_estudiante', blank=True, null=True)
    unidad_educativa = models.CharField(max_length=100, blank=True, null=True)
    anio_egreso = models.CharField(max_length=100, blank=True, null=True)
    tipo_colegio = models.CharField(max_length=100, blank=True, null=True)
    pais_academico = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'educacion_primaria'


class Estudiante(models.Model):
    ci_estudiante = models.SmallIntegerField(primary_key=True)
    extencion = models.CharField(max_length=20, blank=True, null=True)
    id_carrera = models.ForeignKey(Carrera, models.DO_NOTHING, db_column='id_carrera', blank=True, null=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidop = models.CharField(db_column='apellidoP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellidom = models.CharField(db_column='apellidoM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(max_length=255, blank=True, null=True)
    celular = models.SmallIntegerField(blank=True, null=True)
    genero = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    depa_nacimiento = models.CharField(max_length=50, blank=True, null=True)
    fotografia = models.CharField(max_length=255, blank=True, null=True)
    estado_civil = models.CharField(max_length=50, blank=True, null=True)
    idioma_nativo = models.CharField(max_length=50, blank=True, null=True)
    idioma_regular = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    descripcion_estado = models.CharField(max_length=255, blank=True, null=True)
    baja = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'estudiante'


class IdiomaOriginario(models.Model):
    id = models.SmallAutoField(primary_key=True)
    nombre_idioma = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'idioma_originario'


class MallaAcademica(models.Model):
    id = models.SmallAutoField(primary_key=True)
    id_carrera = models.ForeignKey(Carrera, models.DO_NOTHING, db_column='id_carrera', blank=True, null=True)
    id_asignatura = models.ForeignKey(Asignatura, models.DO_NOTHING, db_column='id_asignatura', blank=True, null=True)
    anio_aprobacion = models.CharField(max_length=10, blank=True, null=True)
    doc_resolucion = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'malla_academica'


class Municipio(models.Model):
    id = models.SmallAutoField(primary_key=True)
    id_provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)
    nombre_municipio = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'municipio'


class NotaEstudiante(models.Model):
    id = models.SmallAutoField(primary_key=True)
    id_asignatura_cursada = models.ForeignKey(AsignaturaCursada, models.DO_NOTHING, db_column='id_asignatura_cursada', blank=True, null=True)
    nota_num_normal = models.SmallIntegerField(blank=True, null=True)
    instancia = models.CharField(max_length=20, blank=True, null=True, db_comment='si/no')
    nota_num_instancia = models.SmallIntegerField(blank=True, null=True)
    nota_num_final = models.SmallIntegerField(blank=True, null=True)
    nota_literal_espaniol = models.CharField(max_length=100, blank=True, null=True)
    nota_literal_quechua = models.CharField(max_length=100, blank=True, null=True)
    gestion = models.CharField(max_length=20, blank=True, null=True)
    observacion = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nota_estudiante'


class NumerosLetras(models.Model):
    id = models.SmallAutoField(primary_key=True)
    numeral = models.SmallIntegerField(blank=True, null=True)
    literal_espaniol = models.CharField(max_length=100, blank=True, null=True)
    literal_quechua = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'numeros_letras'


class Organizacion(models.Model):
    id = models.SmallAutoField(primary_key=True)
    ci_estudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='ci_estudiante', blank=True, null=True)
    organizacion_matriz = models.CharField(max_length=100, blank=True, null=True)
    organizacion_departamental = models.CharField(max_length=100, blank=True, null=True)
    organizacion_regional = models.CharField(max_length=100, blank=True, null=True)
    comunidad_sindicato = models.CharField(max_length=100, blank=True, null=True)
    otros = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'organizacion'


class Provincia(models.Model):
    id = models.SmallAutoField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    nombre_provincia = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'provincia'


class ResponsableEstudiante(models.Model):
    id = models.SmallAutoField(primary_key=True)
    ci_estudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='ci_estudiante', blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellidop = models.CharField(db_column='apellidoP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    apellidom = models.CharField(db_column='apellidoM', max_length=100, blank=True, null=True)  # Field name made lowercase.
    ci = models.SmallIntegerField(blank=True, null=True)
    celular = models.SmallIntegerField(blank=True, null=True)
    ocupacion = models.CharField(max_length=255, blank=True, null=True)
    idioma = models.CharField(max_length=50, blank=True, null=True)
    relacion_responsable = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'responsable_estudiante'
