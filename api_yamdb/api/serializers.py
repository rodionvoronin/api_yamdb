from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField, ValidationError,
    PrimaryKeyRelatedField,
)
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Review, Comment

User = get_user_model()


class TitleSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    review = PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', 'author')