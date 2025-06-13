from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from adopciones.models import Publicacion, RegistroVoluntarios, UsuarioPersonalizado
from adopciones.formularios import RegistroUsuarioForm, RegistroVoluntariosForm, MascotaForm, EditarUsuarioForm, PublicacionForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.views.generic import UpdateView, DeleteView, CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login, PasswordChangeView
from django.http import HttpResponseForbidden
from ENTREGA_FINAL_PROYECTO import settings

from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Mascota, CasoAdoptado
from .formularios import CasoAdoptadoForm
from datetime import date

from django.views.generic import ListView
from .models import CasoAdoptado

from django.db.models import Q

# Create your views here.

def acerca_de_mi(request):
    return render(request, 'adopciones/acerca_de_mi.html')

def gallery(request):
    return render(request, 'adopciones/gallery.html')

def index(request):
    return render(request, 'adopciones/index.html')

def contact(request):
    return render(request, 'adopciones/contact.html')

def about (request):
    return render(request, 'adopciones/about.html')


def publicaciones(request):
    query = request.GET.get('q')
    print('Query:', query)  # para el buscador y que me deje los resultados
    if query:
        publicaciones = Publicacion.objects.filter(
            Q(titulo_publicacion__icontains=query) |
            Q(contenido_publicacion__icontains=query) |
            Q(mascota_publicacion__nombre__icontains=query) |
            Q(mascota_publicacion__raza__icontains=query) |
            Q(mascota_publicacion__tipo__icontains=query)
        ).order_by('-fecha_publicacion')
    else:
        publicaciones = Publicacion.objects.all().order_by('-fecha_publicacion')
    print('Publicaciones encontradas:', publicaciones.count())  
    return render(request, "adopciones/publicaciones.html", {"publicaciones": publicaciones})


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarUsuarioForm(instance=request.user)
    return render(request, 'adopciones/editar_perfil.html', {'form': form})

    


@login_required
def perfil(request):
    return render(request, 'adopciones/perfil.html', {'usuario': request.user})


    
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'adopciones/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'adopciones/login.html')

@require_POST
def logout_usuario(request):
    logout(request)
    return redirect('index')


def registrar_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save()

            # Crea publicacion automatica y pasa a adopciones, ver despues de cambiar esto, para que haya instancia de evaluaciòn y aprobacion de la publicacion
            Publicacion.objects.create(
                titulo_publicacion=f"{mascota.nombre}",
                contenido_publicacion=f"{mascota.descripcion}",
                mascota_publicacion=mascota
            )
            return redirect('index')
    else:
        form = MascotaForm()
    return render(request, 'adopciones/registrar_mascota.html', {'form': form})


class SoloAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('index')


class AdminRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    login_url = settings.LOGIN_URL  # toma la url del settings.py 

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # redirige al login configurado en settings.LOGIN_URL
            return redirect_to_login(self.request.get_full_path(), login_url=self.login_url)
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")

#cruds
class PublicacionUpdateView(AdminRequiredMixin, UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'adopciones/publicacion_form.html'  
    success_url = reverse_lazy('publicaciones')

class PublicacionDeleteView(AdminRequiredMixin, DeleteView):
    model = Publicacion
    template_name = 'adopciones/publicacion_confirm_delete.html'  
    success_url = reverse_lazy('publicaciones')

class VoluntarioListView(LoginRequiredMixin, ListView):
    model = RegistroVoluntarios
    template_name = 'adopciones/registro_voluntarios/lista.html'
    context_object_name = 'voluntarios'

class VoluntarioCreateView(LoginRequiredMixin, CreateView):
    model = RegistroVoluntarios
    form_class = RegistroVoluntariosForm
    template_name = 'adopciones/registro_voluntarios/formulario.html'
    success_url = reverse_lazy('voluntarios_lista')

class VoluntarioUpdateView(AdminRequiredMixin, UpdateView):
    model = RegistroVoluntarios
    form_class = RegistroVoluntariosForm
    template_name = 'adopciones/registro_voluntarios/formulario.html'
    success_url = reverse_lazy('voluntarios_lista')

class VoluntarioDeleteView(AdminRequiredMixin, DeleteView):
    model = RegistroVoluntarios
    template_name = 'adopciones/registro_voluntarios/eliminar.html'
    success_url = reverse_lazy('voluntarios_lista')

class UsuarioCreateView(CreateView):
    model = UsuarioPersonalizado
    form_class = RegistroUsuarioForm
    template_name = 'adopciones/registro_usuario.html'
    success_url = reverse_lazy('usuarios_lista')

class UsuarioUpdateView(SoloAdminMixin, UpdateView):
    model = UsuarioPersonalizado
    form_class = RegistroUsuarioForm
    template_name = 'adopciones/registro_usuario.html'
    success_url = reverse_lazy('usuarios_lista')

class CambiarPasswordView(PasswordChangeView):
    login_url = settings.LOGIN_URL  # ver porque django rompe y manda a pagina predeterminada, pongo para que tome la url del settings.py 
    template_name = 'adopciones/cambiar_password.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)  # Cierra sesion
        return response

class UsuarioDeleteView(SoloAdminMixin, DeleteView):
    model = UsuarioPersonalizado
    template_name = 'adopciones/usuarios_eliminar.html'
    success_url = reverse_lazy('usuarios_lista')

class UsuarioListView(SoloAdminMixin, ListView):
    model = UsuarioPersonalizado
    template_name = 'adopciones/usuarios_lista.html'
    context_object_name = 'usuarios'


class RegistrarAdopcionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, mascota_id):
        mascota = get_object_or_404(Mascota, id=mascota_id)
        if not mascota.adoptada:
            mascota.adoptada = True
            mascota.save()

            publicacion = Publicacion.objects.filter(mascota_publicacion=mascota).first()

            CasoAdoptado.objects.create(
                mascota=mascota,
                fecha_adopcion=date.today(),
                comentarios=f"Adoptado desde publicación: {publicacion.titulo_publicacion}" if publicacion else ""
            )

            messages.success(request, f"{mascota.nombre} fue marcada como adoptada.")
        else:
            messages.info(request, f"{mascota.nombre} ya estaba marcada como adoptada.")

        return redirect('publicaciones')

class ListaAdoptadosView(ListView):
    model = CasoAdoptado
    template_name = 'adopciones/lista_adoptados.html'
    context_object_name = 'casos'

