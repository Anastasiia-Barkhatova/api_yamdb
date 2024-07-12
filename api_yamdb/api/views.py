from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filter import TitleFilter
from api.permission import (
    IsAdminOrModeratorOrAuthor,
    IsAuthenticatedAdminOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from reviews.models import Category, Comment, Genre, Review, Title


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Представление для категорий."""

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Представление для жанров."""

    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (IsAuthenticatedAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для произведений."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
    permission_classes = (IsAuthenticatedAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    pagination_class = PageNumberPagination
    filterset_fields = ('genre__slug',)
    filterset_class = TitleFilter
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментариев."""

    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminOrModeratorOrAuthor,
        IsAuthenticatedOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all().order_by('-pub_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminOrModeratorOrAuthor,
        IsAuthenticatedOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all().order_by('-pub_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
