from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField, ValidationError,
    PrimaryKeyRelatedField
)
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Comment

User = get_user_model()


class TitleSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


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