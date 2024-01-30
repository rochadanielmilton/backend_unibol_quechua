from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from.import views
router = DefaultRouter()
router.register(r'carreras',CarreraView, basename='carrera')
router.register(r'municipios',MunicipioView, basename='municipios')
router.register(r'provincias',ProvinciaView, basename='provincias')
router.register(r'departamentos',DepartamentoView, basename='departamentos')
router.register(r'idiomasOriginarios',IdiomaOriginarioView, basename='idiomasOriginarios')
router.register(r'aniosCarreras',AnioCarreraView, basename='aniosCarreras')
router.register(r'numerosLetras',NumerosLetrasView, basename='numerosLetras')
router.register(r'asignaturas',AsignaturaView, basename='asignaturas')

urlpatterns = [
    path('', include(router.urls)),
    path('actualizar', views.actualizar_tablas, name='actualizar'),

    
]

urlpatterns += router.urls
