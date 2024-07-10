from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.constants import NAME_LENGHT
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        lookup_field = 'slug'
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=NAME_LENGHT)
    genres = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()
    # rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genres',
            'category'
        )

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        rating = reviews.aggregate(Avg('score'))['score__avg']
        return rating


class TitleWriteSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
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
            'name', 'year', 'description', 'genres', 'category')

    def to_representation(self, title):
        serializer = TitleReadSerializer(title)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
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
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
