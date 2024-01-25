from django.shortcuts import render
from rest_framework import viewsets
from parametros.models import Docente
from .serializers import DocenteSerializer



class DocenteView(viewsets.ModelViewSet):
    queryset=Docente.objects.all()
    serializer_class=DocenteSerializer