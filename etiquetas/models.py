from django.contrib.auth.models import User
from django.db import models
import datetime

class Endereco(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orgao = models.CharField(max_length = 100)
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    cidade = models.CharField(max_length = 100)
    cep = models.CharField(max_length = 9)
    estado = models.CharField(max_length = 100)

    def __str__(self):
        return '{} - {} - {} - {} - {} - {}'.format(self.orgao, self.rua, self.numero, self.cep, self.cidade, self.estado)

class Destinatario(models.Model):
    
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)    
    nome = models.CharField(max_length = 100)  
    funcao = models.CharField(max_length = 100)  
    email = models.EmailField(max_length = 100)
    orgao = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    
    data_adicionado = models.DateTimeField(auto_now_add=True)
    data_gerado = models.DateTimeField(null=True)    

    def __str__(self):
        return self.nome