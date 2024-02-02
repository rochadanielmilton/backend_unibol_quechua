from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from.import views

urlpatterns = [
  
    path('obtenerEstudiantesInscripcion/', views.ObtenerEstudiantesInscripcion, name='obtenerEstudiantesInscripcion'),
    path('obtenerAsignaturasNoCursadas/<int:ci_estudiante>/', views.ObenerAsignaturasNoCursadas, name='obtenerAsignaturasNoCursadas'),
    path('inscribirEstudiante/', views.inscribirEstudiante, name='inscribirEstudiante'),
    
       
]
