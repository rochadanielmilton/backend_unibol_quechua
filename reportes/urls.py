from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from.import views

urlpatterns = [
    path('EstudiantesCarreraAnio/<str:codigo_carrera>/<str:anio_cursado>/', views.EstudiantesCarreraAnio, name='EstudiantesCarreraAnio'),
    path('EstudiantesInscritosGenero/', views.EstudiantesInscritosGenero, name='EstudiantesInscritosGenero'), 

    
]
    