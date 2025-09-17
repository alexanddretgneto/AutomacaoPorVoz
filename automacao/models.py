from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.CharField(max_length=20)
    frequencia = models.FloatField(default=0.0)  # frequência em %
    notas = models.JSONField(default=list)       # notas por aula, lista de floats

    def __str__(self):
        return f"{self.nome} ({self.ano})"
