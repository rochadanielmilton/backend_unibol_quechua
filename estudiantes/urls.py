from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from.import views

router = DefaultRouter()
router.register(r'estudiantes',EstudianteRegularesView, basename='estudiante')
router.register(r'documentacionEstudiante',DocumentacionEstudianteView, basename='documentacionEstudiante')
router.register(r'organizacion',OrganizacionView, basename='organizacion')
router.register(r'responsableEstudiante',ResponsableEstudianteView, basename='responsableEstudiante')
router.register(r'educacionPrimaria',EducacionPrimariaView, basename='educacionPrimaria')
router.register(r'asignaturaCursada',AsignaturaCursadaView, basename='asignaturaEstudiante')
router.register(r'notaEstudiante',NotaEstudianteView, basename='notaEstudiante')



urlpatterns = [
    path('',include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('obtenerAsignaturasCursadas/<int:ci_estudiante>/', views.ObtenerHitorialAcademico, name='obtenerAsignaturasCursadas'),
    #path('obtenerAsignaturasAprobadas/<int:ci_estudiante>/', views.ObtenerMateriasAprobadas, name='obtenerAsignaturasAprobadas'),
    path('subirNota/<int:ci_estudiante>/', views.subirNota, name='subirNota'),   
    path('formularioAdmision/<int:ci_estudiante>/', views.formularioAdmision, name='formularioAdmision'),
    #path('obtenerCertificacionGestionAnterior/<int:ci_estudiante>/', views.obtenerCertificacionGestionAnterior, name='obtenerCertificacionGestionAnterior'), 
    path('obtenerCertificacionPorGestion/<int:ci_estudiante>/<str:anio>/', views.obtenerCertificacionPorGestion, name='obtenerCertificacionPorGestion'), 
    path('ObtenerHitorialAcademico2/<int:ci_estudiante>/', views.ObtenerHitorialAcademico2, name='ObtenerHitorialAcademico2'),
    path('ObtenerHitorialAcademicoAvanceGeneral/<int:ci_estudiante>/', views.ObtenerHitorialAcademicoAvanceGeneral, name='ObtenerHitorialAcademicoAvanceGeneral'),

    path('ObtenerEducacionPrimaria/<int:ci_estudiante>/', views.ObtenerEducacionPrimaria, name='ObtenerEducacionPrimaria'),
    path('ObtenerResponsable/<int:ci_estudiante>/', views.ObtenerResponsable, name='ObtenerResponsable'),
    path('ObtenerOrganizacion/<int:ci_estudiante>/', views.ObtenerOrganizacion, name='ObtenerOrganizacion'),

    path('editarOrganizacion/<int:pk>/', views.EditarOrganizacion.as_view(), name='editarOrganizacion'),
    path('editarResponsableEstudiante/<int:pk>/', views.EditarResponsableEstudiante.as_view(), name='editarResponsableEstudiante'),
    path('editarEducacionPrimaria/<int:pk>/', views.EditarEducacionPrimaria.as_view(), name='editarEducacionPrimaria'),
    

    
    
    #path('actualizarNotas/', views.ActualizarNotas, name='actualizarNotas'),
    
    
]