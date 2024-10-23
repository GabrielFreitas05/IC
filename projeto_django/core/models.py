from django.db import models

class Usuario(models.Model):
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)
    nome = models.CharField(max_length=255, default='Sem Nome')


    def __str__(self):
        return self.nome

class Teste(models.Model):
    equipamentos = models.CharField(max_length=255, null=True, blank=True)
    om_responsavel = models.CharField(max_length=255, null=True, blank=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)
    descricao = models.DateTimeField(null=True, blank=True)
    resultado = models.DateTimeField(null=True, blank=True)
    usuario = models.DateTimeField(null=True, blank=True)



    def __str__(self):
        return self.descricao
    from django.db import models

