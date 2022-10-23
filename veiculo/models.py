from pickle import FALSE
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

LISTA_STATUS_VEICULO = (
    ("OCUPADO", "Ocupado"),
    ("LIVRE", "Livre"),
    ("PENDENTE", "Pendente"),
)

LISTA_STATUS_VIAGEM = (
    ("FINALIZADA", "Finalizada"),
    ("PENDENTE", "Pendente"),
)

class Veiculo(models.Model):
    modelo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    ano = models.CharField(max_length=4)
    placa = models.CharField(max_length=7)
    cor = models.CharField(max_length=10)
    kilometragem = models.FloatField(default=0)
    KM_Revisao = models.FloatField(default=0)
    status = models.CharField(max_length=15, blank=False, null=True,choices=LISTA_STATUS_VEICULO)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.modelo, self.placa)

class Usuario(AbstractUser):
    CPF = models.CharField(max_length=14)
    CNH = models.CharField(max_length=10)
    categoria = models.CharField(max_length=2)

class Viagem(models.Model):      
    veiculo = models.ForeignKey(Veiculo, null=True,blank=False ,on_delete=models.SET_NULL, limit_choices_to= {'status': 'LIVRE'})
    motorista = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    KM_Inicial = models.FloatField(default=0)
    KM_Final = models.FloatField(default=0,blank=True)
    origem = models.CharField(max_length=50)
    destino = models.CharField(max_length=50,blank=True)
    destino2 = models.CharField(max_length=50,blank=True)
    destino3 = models.CharField(max_length=50,blank=True)
    Data_Hora_Inicio = models.DateTimeField()
    Data_Hora_Fim = models.DateTimeField(null=True)
    status = models.CharField(max_length=15, blank=True, null=False,choices=LISTA_STATUS_VIAGEM)
    fotos = models.ImageField(upload_to='imagens_carros_viagens/')
    

    def __str__(self):
        return "{} - {}".format(self.veiculo, self.Data_Hora_Inicio)


class Revisao(models.Model):      
    veiculo = models.ForeignKey(Veiculo, null=True, on_delete=models.SET_NULL)
    KM = models.FloatField(default=0)    
    Data = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "{} - {} KM".format(self.veiculo, self.KM)

       
