from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstudianteView,CarreraView

router = DefaultRouter()
router.register(r'estudiantes', EstudianteView, basename='estudiante')
router.register(r'carreras',CarreraView, basename='carrera')

urlpatterns = [
    path('', include(router.urls)),
]
