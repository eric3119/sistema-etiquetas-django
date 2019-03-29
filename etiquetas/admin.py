from django.contrib import admin
from .models import Destinatario, Endereco, UserProfile, Orgao

admin.site.register(Destinatario)
admin.site.register(Endereco)
admin.site.register(UserProfile)
admin.site.register(Orgao)