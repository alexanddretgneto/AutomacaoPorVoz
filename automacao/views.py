import re
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Aluno
from .serializers import AlunoSerializer

# ----------------------------
# View raiz /api/automacao/ com HTML
# ----------------------------
class AutomacaoRootView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Renderiza página HTML com textarea e botões Gravar / Parar / Salvar
        """
        return render(request, 'automacao/automacao_root.html')

    def handle_exception(self, exc):
        """
        Mensagem amigável se não estiver logado
        """
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

# ----------------------------
# Endpoint POST único para adicionar aluno
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def adicionar_aluno(request):
    """
    Recebe comando de voz convertido para texto e cria um aluno no banco.
    Exemplo de comando:
    "aluno: alex neto, ano: 2°, notas: 5.0, 6.0, 7.0, frequencia: 80"
    """
    comando = request.data.get('comando', '').strip()
    if not comando:
        return Response({"erro": "Nenhum comando enviado"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Regex para extrair os dados
        pattern = (
            r"aluno:\s*(?P<nome>.*?),\s*"
            r"ano:\s*(?P<ano>.*?),\s*"
            r"notas:\s*(?P<notas>[\d.,\s]+),\s*"
            r"frequencia:\s*(?P<freq>[\d.]+)"
        )
        match = re.match(pattern, comando, re.IGNORECASE)
        if not match:
            return Response({"erro": "Formato do comando inválido"}, status=status.HTTP_400_BAD_REQUEST)

        nome = match.group('nome').strip()
        ano = match.group('ano').strip()
        notas = [float(n.strip()) for n in match.group('notas').split(',')]
        frequencia = float(match.group('freq'))

        # Cria aluno
        aluno = Aluno.objects.create(nome=nome, ano=ano, notas=notas, frequencia=frequencia)
        serializer = AlunoSerializer(aluno)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"erro": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
