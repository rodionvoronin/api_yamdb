from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField, ValidationError
)
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Review

User = get_user_model()


class TitleSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review