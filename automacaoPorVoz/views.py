from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

def api_root(request):
    html = """
    <h1>Bem-vindo ao Portal de Automação Por Voz</h1>
    <ul>
        <li><a href='/api/auth/register/'>Registrar Usuário</a></li>
        <li><a href='/api/auth/login/'>Login</a></li>
        <li><a href='/api/automacao/'>Registros de alunos por Voz</a></li>
    </ul>
    """
    return HttpResponse(html)