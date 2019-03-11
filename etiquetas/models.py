from django.db import models
import datetime

class Etiqueta(models.Model):
    nome = models.CharField(max_length = 100)  
    funcao = models.CharField(max_length = 100)  
    email = models.EmailField(max_length = 100)
    orgao = models.CharField(max_length = 100)
    endereco = models.CharField(max_length = 100)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome