from django.urls import path
from .views import AutomacaoRootView, adicionar_aluno

urlpatterns = [
    path('', AutomacaoRootView.as_view(), name='automacao_root'),
    path('adicionar/', adicionar_aluno, name='adicionar_aluno'),
]
