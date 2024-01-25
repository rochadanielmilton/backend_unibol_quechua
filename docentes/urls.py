from django.urls import path,include
from rest_framework.routers import DefaultRouter
from.views import DocenteView

router = DefaultRouter()
router.register(r'docentes',DocenteView, basename='docentes')

urlpatterns = [
    path('',include(router.urls)),
]