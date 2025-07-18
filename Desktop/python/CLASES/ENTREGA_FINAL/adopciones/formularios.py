from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsuarioPersonalizado, Mascota, Publicacion, RegistroVoluntarios, CasoAdoptado, MensajeContacto

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'avatar', 'edad', 'telefono']

class EditarUsuarioForm(UserChangeForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar', 'edad', 'telefono']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            # Oculta el password      
        if 'password' in self.fields:
            del self.fields['password']
        if 'avatar' in self.fields:
            # Oculta el checkbox de "Clear"
            self.fields['avatar'].widget.clear_checkbox_label = ''
            self.fields['avatar'].widget.template_name = 'widgets/custom_clearable_file_input.html'


class RegistroVoluntariosForm(forms.ModelForm):
    class Meta:
        model = RegistroVoluntarios
        fields = ['nombre', 'apellido', 'zona', 'edad', 'telefono', 'email']


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'edad', 'raza', 'descripcion', 'tipo', 'imagen']


class PublicacionForm(forms.ModelForm):
    nombre = forms.CharField()
    edad = forms.IntegerField()
    descripcion = forms.CharField(widget=forms.Textarea)
    raza = forms.CharField()
    tipo = forms.ChoiceField(choices=Mascota._meta.get_field('tipo').choices)
    imagen = forms.ImageField(required=False)

    class Meta:
        model = Publicacion
        fields = ['titulo_publicacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.mascota_publicacion:
            mascota = self.instance.mascota_publicacion
            self.fields['nombre'].initial = mascota.nombre
            self.fields['edad'].initial = mascota.edad
            self.fields['descripcion'].initial = mascota.descripcion
            self.fields['raza'].initial = mascota.raza
            self.fields['tipo'].initial = mascota.tipo
            self.fields['imagen'].initial = mascota.imagen

    def save(self, commit=True):
        publicacion = super().save(commit=False)
        mascota = publicacion.mascota_publicacion
        mascota.nombre = self.cleaned_data['nombre']
        mascota.edad = self.cleaned_data['edad']
        mascota.descripcion = self.cleaned_data['descripcion']
        mascota.raza = self.cleaned_data['raza']
        mascota.tipo = self.cleaned_data['tipo']
        if self.cleaned_data.get('imagen'):
            mascota.imagen = self.cleaned_data['imagen']
        if commit:
            mascota.save()
            publicacion.save()
        return publicacion

class CasoAdoptadoForm(forms.ModelForm):
    class Meta:
        model = CasoAdoptado
        fields = ['fecha_adopcion', 'adoptante_nombre', 'comentarios', 'activo']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ocultamos el campo mascota si ya hay instancia
        if self.instance and self.instance.mascota:
            self.fields['mascota'] = forms.ModelChoiceField(
                queryset=Mascota.objects.all(),
                initial=self.instance.mascota,
                widget=forms.HiddenInput(),
                required=False
            )


class MensajeContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['mensaje', 'padre']
        widgets = {
            'mensaje': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Escribí tu mensaje...'
            }),
            'padre': forms.HiddenInput()
        }