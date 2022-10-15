from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User

from .serializers import SignupSerializer, TokenSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Регистрирует нового пользователя по username и email.
    Присылает на email confirmation_code
    """
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = serializer.data['username']
        email = serializer.data['email']
        user = User(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_email(email, confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Выдаёт токен по username и confirmation_code"""
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(
            user, serializer.data['confirmation_code']
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = confirmation_code_generator(user)
        return Response({"token": token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def confirmation_code_generator(user):
    """Генератор токена"""
    return str(RefreshToken.for_user(user).access_token)


def send_email(email, confirmation_code):
    """Функция отправки электронного письма на адрес пользователя"""
    send_mail(
        subject='confirmation code for get token',
        message=confirmation_code,
        from_email='from@api_yamdb.com',
        recipient_list=[email],
        fail_silently=False,
    )
