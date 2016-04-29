from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User,Group


# Create your models here.
class Beneficiado(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    user = models.OneToOneField(User,related_name='+') #User doesn't has Beneficiado

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]


class Presenca(models.Model):
    beneficiado = models.ForeignKey('Beneficiado')
    data = models.DateField(default=timezone.now)
    chegada = models.TimeField()
    saida = models.TimeField(null=True)
    atualizacao = models.DateTimeField(auto_now=True)
    tarefa = models.TextField(verbose_name='Tarefa', null=True, blank=True)

    def duracao(self):
        if self.saida == None:
            return timezone.timedelta()
        agora = timezone.now()
        chegada = timezone.datetime(year=agora.year,month=agora.month,day=agora.month,hour=self.chegada.hour, minute=self.chegada.minute)
        saida = timezone.datetime(year=agora.year,month=agora.month,day=agora.month,hour=self.saida.hour, minute=self.saida.minute)
        return saida-chegada

    def __str__(self):
        return self.beneficiado.nome+"-"+self.data.__str__()

class Frequencia(models.Model):
    beneficiado = models.ForeignKey('Beneficiado')
    mes = models.SmallIntegerField()
    ano = models.SmallIntegerField()
    atualizacao = models.DateTimeField(auto_now=True)

    def carga_horaria(self):
        total = timezone.timedelta()
        for p in self.presenca_set.all():
            total += p.duracao()
        #79200 segundos = 22h
        if(total.total_seconds() >= 79200) :
            total = total + timezone.timedelta(hours=8)

        return total

    def __str__(self):
        return self.beneficiado.nome+"-"+self.mes.__str__()+"/"+self.ano.__str__()

    class Meta:
        ordering = ["-id"]