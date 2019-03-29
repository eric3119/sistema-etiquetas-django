from django.contrib.auth.models import User
from django.db import models
import datetime

class Endereco(models.Model):    
    rua = models.CharField(max_length=100)
    numero = models.PositiveIntegerField()
    cidade = models.CharField(max_length = 100)
    cep = models.CharField(max_length = 9)
    estado = models.CharField(max_length = 100)

    def __str__(self):
        return '{} - {} - {} - {} - {}'.format(self.rua, self.numero, self.cep, self.cidade, self.estado)


class Orgao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    funcao = models.CharField(max_length = 100)
    orgao = models.ForeignKey(Orgao, on_delete=models.CASCADE)

    # def __str__(self):
    #     return self.user.__str__()
    

class Destinatario(models.Model):
    
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length = 100)
    funcao = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    orgao = models.ForeignKey(Orgao, on_delete=models.CASCADE)
    
    data_adicionado = models.DateTimeField(auto_now_add=True)
    data_gerado = models.DateTimeField(null=True)

    def __str__(self):
        return self.nome