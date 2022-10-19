from ast import Mod
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import ADMINS_EMAIL
from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import AdminViewMixin, ModeratorViewMixin
from .permissions import IsAdminOrSuperUser
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTitleSerializer,
                          ReviewSerializer, SignupSerializer, TitleSerializer,
                          TokenSerializer, UserPatchMeSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrSuperUser,)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = (
        DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter
    )
    search_fields = ('username',)
    ordering = ('username',)

    @action(
        methods=['GET', 'PATCH'],
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


class SignUpView(APIView):
    """
    Регистрирует нового пользователя по username и email.
    Присылает на email confirmation_code.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, _ = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='confirmation code for get token',
            message=f'Your confirmation code: "{confirmation_code}"',
            from_email=ADMINS_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(SignUpView):
    """Выдаёт токен по username и confirmation_code"""

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']
        ):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token = str(RefreshToken.for_user(user).access_token)
        return Response({"token": token}, status=status.HTTP_200_OK)


class CategoryViewSet(
        mixins.CreateModelMixin, mixins.DestroyModelMixin,
        mixins.ListModelMixin, AdminViewMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    ordering = ('name',)


class GenreViewSet(CategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet, AdminViewMixin):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).select_related()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_class = TitleFilter
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet, ModeratorViewMixin):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter,)
    ordering = ('-pub_date')

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all().select_related('author')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ReviewViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(title.reviews, id=review_id)
        return review.comments.all().select_related('author')

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
