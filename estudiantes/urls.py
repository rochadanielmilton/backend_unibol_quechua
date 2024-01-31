from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from.import views

router = DefaultRouter()
router.register(r'estudiantes',EstudianteView, basename='estudiante')
router.register(r'documentacionEstudiante',DocumentacionEstudianteView, basename='documentacionEstudiante')
router.register(r'organizacion',OrganizacionView, basename='organizacion')
router.register(r'responsableEstudiante',ResponsableEstudianteView, basename='responsableEstudiante')
router.register(r'educacionPrimaria',EducacionPrimariaView, basename='educacionPrimaria')
router.register(r'asignaturaCursada',AsignaturaCursadaView, basename='asignaturaEstudiante')
router.register(r'notaEstudiante',NotaEstudianteView, basename='notaEstudiante')



urlpatterns = [
    path('',include(router.urls)),
    path('obtenerAsignaturasNoCursadas/<int:ci_estudiante>/', views.ObenerAsignaturasNoCursadas, name='obtenerAsignaturasNoCursadas'),
    path('obtenerAsignaturasCursadas/<int:ci_estudiante>/', views.ObtenerHitorialAcademico, name='obtenerAsignaturasCursadas'),
    path('obtenerAsignaturasAprobadas/<int:ci_estudiante>/', views.ObtenerMateriasAprobadas, name='obtenerAsignaturasAprobadas'),
    
    #path('actualizarNotas/', views.ActualizarNotas, name='actualizarNotas'),
    
    
]