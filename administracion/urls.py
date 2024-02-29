from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from.import views

urlpatterns = [
  
    path('obtenerEstudiantesInscripcion/', views.ObtenerEstudiantesInscripcion, name='obtenerEstudiantesInscripcion'),
    path('obtenerAsignaturasNoCursadas/<int:ci_estudiante>/', views.ObenerAsignaturasNoCursadas, name='obtenerAsignaturasNoCursadas'),
    path('inscribirEstudiante/', views.inscribirEstudiante, name='inscribirEstudiante'),
    path('obtenerPostulates/', views.ObtenerPostulates, name='obtenerPostulates'),
    path('registrarNueboEstudiante/<int:ci_postulante>/', views.RegistrarNueboEstudiante, name='registrarNueboEstudiante'),
    path('eliminarDatos/<int:ci_estudiante>/', views.EliminarDatos, name='eliminarDatos'),
    path('inscribirEstudiantePrimerAnio/<int:ci_estudiante>/', views.InscribirEstudiantePrimerAnio, name='inscribirEstudiantePrimerAnio'),
    path('reimprimirInscripcion/<int:ci_estudiante>/', views.reimprimirInscripcion, name='reimprimirInscripcion'),
    path('cancelarInscripcion/<int:ci_estudiante>/', views.cancelarInscripcion, name='cancelarInscripcion'),  
    path('inscripcionParaDefensa/<int:ci_estudiante>/', views.inscripcionParaDefensa, name='inscripcionParaDefensa'),  
    
       
]
