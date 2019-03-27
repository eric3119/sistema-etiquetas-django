from django.contrib import admin
from .models import Destinatario, Endereco#, Remetente

admin.site.register(Destinatario)
admin.site.register(Endereco)
# admin.site.register(Remetente)