from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.urls import reverse
from adopciones.models import Publicacion, RegistroVoluntarios, UsuarioPersonalizado, MensajeContacto, Mascota, CasoAdoptado
from adopciones.formularios import RegistroUsuarioForm, RegistroVoluntariosForm, MascotaForm, EditarUsuarioForm, PublicacionForm, MensajeContactoForm, CasoAdoptadoForm
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
from django.urls import reverse_lazy
from datetime import date

from django.views.generic import ListView

from .models import MensajeContacto
from django.core.paginator import Paginator

from django.shortcuts import redirect
from django.urls import reverse

from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import MensajeContacto
from .formularios import MensajeContactoForm


# Create your views here.

def acerca_de_mi(request):
    return render(request, 'adopciones/acerca_de_mi.html')

def gallery(request):
    return render(request, 'adopciones/gallery.html')

def index(request):
    return render(request, 'adopciones/index.html')

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
    return render(request, 'adopciones/index.html', {'usuario': request.user})

    
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')  
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'¡Bienvenid@, {user.username or user.first_name}!')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect('login')  # o return render(...)

    return render(request, 'adopciones/login.html')


@require_POST
def logout_usuario(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
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
    success_url = reverse_lazy('index')

class VoluntarioDeleteView(AdminRequiredMixin, DeleteView):
    model = RegistroVoluntarios
    template_name = 'adopciones/registro_voluntarios/eliminar.html'
    success_url = reverse_lazy('voluntarios_lista')

class UsuarioCreateView(CreateView):
    model = UsuarioPersonalizado
    form_class = RegistroUsuarioForm
    template_name = 'adopciones/registro_usuario.html'
    success_url = reverse_lazy('login')

class UsuarioUpdateView(SoloAdminMixin, UpdateView):
    model = UsuarioPersonalizado
    form_class = RegistroUsuarioForm
    template_name = 'adopciones/registro_usuario.html'
    success_url = reverse_lazy('index')

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

class EliminarAdoptadoView(UserPassesTestMixin, DeleteView):
    model = CasoAdoptado
    template_name = 'adopciones/eliminar_adoptado.html'
    success_url = reverse_lazy('lista_adoptados')

    def test_func(self):
        return self.request.user.is_superuser


class EditarAdoptadoView(UserPassesTestMixin, UpdateView):
    model = CasoAdoptado
    form_class = CasoAdoptadoForm
    template_name = 'adopciones/editar_adoptado.html'
    success_url = reverse_lazy('lista_adoptados')

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['mascota_form'] = MascotaForm(self.request.POST, self.request.FILES, instance=self.object.mascota)
        else:
            context['mascota_form'] = MascotaForm(instance=self.object.mascota)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        mascota_form = context['mascota_form']
        
        if mascota_form.is_valid():
            self.object = form.save(commit=False)
            mascota = mascota_form.save()

            # Si el caso se desactiva, devolvemos la mascota a adopción
            if not self.object.activo:
                mascota.adoptada = False
                mascota.save()

                # Creamos una nueva publicación
                Publicacion.objects.create(
                    titulo_publicacion=f"{mascota.nombre}",
                    contenido_publicacion=mascota.descripcion,
                    mascota_publicacion=mascota
                )

                self.object.delete()
                messages.success(self.request, f"{mascota.nombre} volvió a estar en adopción y se publicó correctamente.")
                return redirect('publicaciones')

            # Si el caso sigue activo, simplemente guardamos
            self.object.save()
            return super().form_valid(form)
        
        return self.form_invalid(form)

    def form_invalid(self, form):
            print(">>> form_invalid")
            print(form.errors)
            return super().form_invalid(form)


def contacto(request):
    mensajes_list = MensajeContacto.objects.filter(padre__isnull=True).order_by('-fecha_envio')
    paginator = Paginator(mensajes_list, 10)
    page_number = request.GET.get('page')
    mensajes = paginator.get_page(page_number)

    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            if request.user.is_authenticated:
                mensaje.usuario = request.user
                mensaje.nombre = request.user.username
                mensaje.save()

                if mensaje.padre:
                    # Calcular en qué página está el padre
                    padre_id = mensaje.padre.id
                    padre_index = list(mensajes_list).index(mensaje.padre)
                    padre_pagina = padre_index // paginator.per_page + 1

                    return redirect(f"{reverse('contact')}?page={padre_pagina}&scroll_to=mensaje-{padre_id}")
                else:
                    return redirect(f"{reverse('contact')}#blog")

            else:
                messages.error(request, "Debes iniciar sesión para enviar un mensaje.")
        else:
            messages.error(request, "Ha ocurrido un error - intenta nuevamente.")
    else:
        form = MensajeContactoForm()

    return render(request, 'adopciones/contact.html', {
        'form': form,
        'mensajes': mensajes,
    })

