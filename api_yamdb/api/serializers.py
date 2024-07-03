from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', 'title')

    def validate(self, data):
        if self.context['request'].method == 'POST' and Review.objects.filter(
            title=self.context['title_id'],
            author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                'Ранее вы уже оставляли отзыв на это произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
