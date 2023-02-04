from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField, ValidationError,
    PrimaryKeyRelatedField, IntegerField,
)
from django.core.validators import MaxValueValidator, MinValueValidator
# from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Review

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
    title_id = self.context['view'].kwargs.get('title_id')
    title = get_object_or_404(Title, pk=title_id)
    score = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        required=True,
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if title.reviews.select_related('title').filter(author=author):
                raise ValidationError(
                    'Отзыв уже существует'
                )

        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title', 'author')
