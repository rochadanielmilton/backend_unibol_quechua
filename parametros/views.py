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

class MunicipioView(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()    
    serializer_class = MunicipioSerializer

class ProvinciaView(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()    
    serializer_class = ProvinciaSerializer

class DepartamentoView(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()    
    serializer_class = DepartamentoSerializer

class IdiomaOriginarioView(viewsets.ModelViewSet):
    queryset = IdiomaOriginario.objects.all()    
    serializer_class = IdiomaOriginarioSerializer

class AnioCarreraView(viewsets.ModelViewSet):
    queryset = AnioCarrera.objects.all()    
    serializer_class = AnioCarreraSerializer

class NumerosLetrasView(viewsets.ModelViewSet):
    queryset = NumerosLetras.objects.all()    
    serializer_class = NumerosLetrasSerializer

