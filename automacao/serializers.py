from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from .models import Aluno

# Serializer para o modelo Aluno
class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'ano', 'frequencia', 'notas']

