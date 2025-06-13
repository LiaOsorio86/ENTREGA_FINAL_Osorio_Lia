from django.contrib import admin

# Register your models here.
from .models import Mascota, Publicacion, RegistroVoluntarios, UsuarioPersonalizado

admin.site.register(Mascota)
admin.site.register(Publicacion)
admin.site.register(RegistroVoluntarios)
admin.site.register(UsuarioPersonalizado)

