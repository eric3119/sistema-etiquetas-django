from django.db import models
import datetime

class Remetente(models.Model):
    nome = models.CharField(max_length = 100)  
    funcao = models.CharField(max_length = 100)  
    email = models.EmailField(max_length = 100)
    orgao = models.CharField(max_length = 100)
    endereco = models.CharField(max_length = 100)    

    def __str__(self):
        return self.nome

class Destinatario(models.Model):
    nome = models.CharField(max_length = 100)  
    funcao = models.CharField(max_length = 100)  
    email = models.EmailField(max_length = 100)
    orgao = models.CharField(max_length = 100)
    endereco = models.CharField(max_length = 100)
    data_adicionado = models.DateTimeField(auto_now_add=True)
    data_gerado = models.DateTimeField(null=True)
    remetente = models.ForeignKey(Remetente, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    