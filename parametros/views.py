from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *


class AsignaturaView(viewsets.ModelViewSet):
    queryset=Asignatura.objects.all()
    serializer_class=AsignaturaSerializer

class MallaAcademicaView(viewsets.ModelViewSet):
    queryset=MallaAcademica.objects.all()
    serializer_class=MallaAcademicaSerializer


class CarreraView(viewsets.ModelViewSet):
    queryset = Carrera.objects.all()    
    serializer_class = CarreraSerializer

