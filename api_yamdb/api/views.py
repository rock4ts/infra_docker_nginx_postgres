from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

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

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Admin, Moderator can manage reviews
    User can manage self reviews
    /titles/{title_id}/reviews/ - get all reviews on title
    /titles/{title_id}/reviews/{id}/ - get title with id
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Admin, Moderator can manage comments
    User can manage self comments
    /titles/{title_id}/reviews/{review_id}/comments/
    get all comments and review with id
    /titles/{title_id}/reviews/{review_id}/comments/{id}/
    git comment with id
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
