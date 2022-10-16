from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User
from rest_framework import viewsets
from .permissions import IsAdminOrSuperuser
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import (
    SignupSerializer, TokenSerializer, UserSerializer, UserPatchMeSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """viewset для работы с пользователями."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperuser,)
    pagination_class = PageNumberPagination
    lookup_field = "username"
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserPatchMeSerializer,
    )
    def my_profile(self, request):
        user = self.request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class signup(APIView):
    """
    Регистрирует нового пользователя по username и email.
    Присылает на email confirmation_code.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.data['username']
            email = serializer.data['email']
            user = get_object_or_404(User, username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='confirmation code for get token',
                message=f'Your confirmation code: "{confirmation_code}"',
                from_email='from@api_yamdb.com',
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class token(APIView):
    """Выдаёт токен по username и confirmation_code"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(
            user, serializer.data['confirmation_code']
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = str(RefreshToken.for_user(user).access_token)
        return Response({"token": token}, status=status.HTTP_200_OK)
