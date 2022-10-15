from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from .filters import TitleFilter
from .serializers import (
    CategorySerializer, GenreSerializer, GetTitleSerializer, TitleSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Category.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Genre.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().select_related('category')
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return GetTitleSerializer
        return TitleSerializer
