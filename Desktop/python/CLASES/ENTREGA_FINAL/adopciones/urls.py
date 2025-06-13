from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'), 
    path('adopciones/gallery/', views.gallery, name='gallery'), 
    path('adopciones/contact/', views.contact, name='contact'),
    path('adopciones/about/', views.about, name='about'),
    path('adopciones/registrar_mascota/', views.registrar_mascota, name='registrar_mascota'), # mascotas en adopcion
    path('adopciones/publicaciones/', views.publicaciones, name='publicaciones'),
    #path('adopciones/voluntarios/', views.registro_voluntarios, name='voluntarios'), #registro de voluntarios entra por crud
    #path('adopciones/registro_usuario/', views.registro_usuario, name='registro_usuario'), # registro entra por crud
    path('adopciones/login/', views.login_usuario, name='login'),
    path('adopciones/logout/', views.logout_usuario, name='logout'),
    path('adopciones/perfil/', views.perfil, name='perfil'),
    path('adopciones/editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('adopciones/acerca_de_mi/', views.acerca_de_mi, name='acerca_de_mi'),

    # CRUDS de publicacion, voluntarios, usuarios y adoptados
    path('publicacion/<int:pk>/editar/', views.PublicacionUpdateView.as_view(), name='publicacion_update'),
    path('publicacion/<int:pk>/eliminar/', views.PublicacionDeleteView.as_view(), name='publicacion_delete'),
    path('voluntarios/<int:pk>/eliminar/', views.VoluntarioDeleteView.as_view(), name='voluntario_eliminar'),
    path('voluntarios/editar/<int:pk>/', views.VoluntarioUpdateView.as_view(), name='voluntario_editar'),
    path('voluntarios/lista/', views.VoluntarioListView.as_view(), name='voluntarios_lista'),
    path('voluntarios/formulario/', views.VoluntarioCreateView.as_view(), name='voluntario_crear'), 
    path('usuarios/usuarios_lista/', views.UsuarioListView.as_view(), name='usuarios_lista'),
    path('usuarios/registro_usuario/', views.UsuarioCreateView.as_view(), name='registro_usuario'),
    path('usuarios/editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('usuarios/eliminar/<int:pk>/', views.UsuarioDeleteView.as_view(), name='usuario_eliminar'),
    #path('login/', auth_views.LoginView.as_view(template_name='adopciones/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('cambiar-password/', views.CambiarPasswordView.as_view(), name='cambiar_password'), # Views para cambiar contraseña
    path('adoptar/<int:mascota_id>/', views.RegistrarAdopcionView.as_view(), name='registrar_adopcion'),
    path('adopciones/lista_adoptados', views.ListaAdoptadosView.as_view(), name='lista_adoptados'),

    ]
