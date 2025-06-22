
from django.db import models
from django.contrib.auth.models import AbstractUser

from ENTREGA_FINAL_PROYECTO import settings
# Create your models here.


class UsuarioPersonalizado(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username

class RegistroVoluntarios(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    zona = models.CharField(max_length=100)
    edad = models.IntegerField()
    telefono = models.IntegerField()
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    descripcion = models.TextField()
    raza = models.CharField(max_length=100, default='Desconocida')
    adoptada = models.BooleanField(default=False)
    tipo = models.CharField(max_length=20, choices=[('perro', 'Perro'), ('gato', 'Gato')])
    imagen = models.ImageField(upload_to='mascotas/', null=True, blank=True)

 
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    

class Publicacion(models.Model):
    titulo_publicacion = models.CharField(max_length=100)
    contenido_publicacion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    mascota_publicacion = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        self.contenido_publicacion = self.mascota_publicacion.descripcion
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo_publicacion


class CasoAdoptado(models.Model):
    mascota = models.OneToOneField(Mascota, on_delete=models.CASCADE)
    fecha_adopcion = models.DateField()
    adoptante_nombre = models.CharField(max_length=100, blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)  # para hacer reverse en la adopcion y volver a publicar
    
    def __str__(self):
        return f"Adopción de {self.mascota.nombre} el {self.fecha_adopcion}"

from django.contrib.auth.models import User

class MensajeContacto(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    padre = models.ForeignKey('self', null=True, blank=True, related_name='respuestas', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre}: {self.mensaje[:30]}"