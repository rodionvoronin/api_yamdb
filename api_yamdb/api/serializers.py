from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer, SlugRelatedField, ValidationError,
    PrimaryKeyRelatedField, IntegerField,
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
    score = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        required=True,
    )

    def validate(self, data):
        if self.context['request'].user == data['reviews']:
            raise serializers.ValidationError(
                'Вы уже писали отзыв на это произведение'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title', 'author')
