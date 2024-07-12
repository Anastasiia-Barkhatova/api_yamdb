from django.db.models import Avg

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.constants import NAME_LENGHT
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на чтение."""
    name = serializers.CharField(max_length=NAME_LENGHT)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        """Вычисление рейтинга."""
        reviews = Review.objects.filter(title=obj)
        rating = reviews.aggregate(Avg('score'))['score__avg']
        return round(rating) if rating is not None else None


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор произведений на запись."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, title):
        serializer = TitleReadSerializer(title)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

    def validate(self, data):
        title_id = self.context['title_id']

        if self.context['request'].method == 'POST' and Review.objects.filter(
            title_id=title_id, author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                "Ранее вы уже оставляли отзыв на данное произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
