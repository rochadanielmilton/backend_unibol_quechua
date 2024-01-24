from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

class EstudianteView(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()    
    serializer_class = EstudianteSerializer
    