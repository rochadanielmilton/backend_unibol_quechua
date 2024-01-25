from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'carreras',CarreraView, basename='carrera')
router.register(r'mallaAcademica',MallaAcademicaView,basename='mallaAcademica')
router.register(r'asignaturas',AsignaturaView, basename='asignaturas')

urlpatterns = [
    path('', include(router.urls)),
]
