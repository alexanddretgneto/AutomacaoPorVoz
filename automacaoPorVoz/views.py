from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

def api_root(request):
    html = """
    <h1>Bem-vindo à API AutomaçãoPorVoz</h1>
    <ul>
        <li><a href='/api/auth/register/'>Registrar usuário</a></li>
        <li><a href='/api/auth/login/'>Login</a></li>
        <li><a href='/api/automacao/'>Automação por voz</a></li>
    </ul>
    """
    return HttpResponse(html)