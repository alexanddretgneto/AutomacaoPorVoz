from django.contrib.auth import authenticate, login
from rest_framework import status, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.models import User


class RegisterView(generics.CreateAPIView):
    """
    Endpoint para registrar usuários via API.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # 🔑 permite acesso sem autenticação

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.get_or_create(user=user)  # cria token DRF


class LoginView(generics.GenericAPIView):
    """
    Endpoint para login via API.
    Retorna token e também cria sessão Django para navegador.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': 'Credenciais inválidas.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Cria sessão Django (login para navegador)
        login(request, user)

        # Cria token DRF
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'username': user.username,
            'token': token.key,
            'session_active': True  # indica que a sessão foi criada
        }, status=status.HTTP_200_OK)
