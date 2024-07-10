from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Comment, Genre, Review, Title

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from .permission import (
    IsAdminOrModeratorOrAuthor,
    IsAuthenticatedOrAdminOrReadOnly,
)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = (
        IsAdminOrModeratorOrAuthor,
        IsAuthenticatedOrReadOnly,
    )
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminOrModeratorOrAuthor,
        IsAuthenticatedOrReadOnly,
    )
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_serializer_context(self):
        return {
            'request': self.request,
            'title_id': self.kwargs.get('title_id'),
        }
