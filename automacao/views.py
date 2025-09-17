from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Aluno
from .serializers import AlunoSerializer
import re
from django.http import HttpResponse

# View raiz /api/automacao/ com autenticação
class AutomacaoRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "mensagem": "Bem-vindo à API de automação por voz!",
            "instrução": "Use o endpoint /api/automacao/adicionar/ para adicionar alunos por comando de voz.",
        })

    def handle_exception(self, exc):
        if getattr(exc, 'status_code', None) == 401:
            html = """
            <h2>Você precisa estar cadastrado e logado para acessar a Automação por Voz</h2>
            <ul>
                <li><a href='/api/auth/register/'>Registrar usuário</a></li>
                <li><a href='/api/auth/login/'>Login</a></li>
            </ul>
            """
            return HttpResponse(html, status=401)
        return super().handle_exception(exc)

# Endpoint para adicionar aluno via comando de voz
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # exige token
def adicionar_aluno(request):
    """
    Recebe comando de voz convertido para texto.
    Exemplo de comando:
    "aluno: alex neto, ano: 2°, notas: 5.0, 6.0, 7.0, frequencia: 80"
    """
    comando = request.data.get('comando', '')

    if not comando:
        return Response({"erro": "Nenhum comando enviado"}, status=400)

    try:
        match = re.match(
            r"aluno:\s*(?P<nome>.*?),\s*ano:\s*(?P<ano>.*?),\s*notas:\s*(?P<notas>[\d.,\s]+),\s*frequencia:\s*(?P<freq>[\d.]+)",
            comando,
            re.IGNORECASE
        )
        if not match:
            return Response({"erro": "Formato do comando inválido"}, status=400)

        nome = match.group('nome').strip()
        ano = match.group('ano').strip()
        notas = [float(n.strip()) for n in match.group('notas').split(',')]
        frequencia = float(match.group('freq'))

        aluno = Aluno.objects.create(nome=nome, ano=ano, notas=notas, frequencia=frequencia)
        serializer = AlunoSerializer(aluno)

        return Response(serializer.data)

    except Exception as e:
        return Response({"erro": str(e)}, status=500)
