from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework.serializers import (
    CharField, EmailField, ModelSerializer, Serializer, SlugRelatedField, ValidationError,
    PrimaryKeyRelatedField, IntegerField
)
from django.core.validators import MaxValueValidator, MinValueValidator
# from rest_framework.validators import UniqueTogetherValidator

import datetime

from reviews.models import Category, Genre, Title, Review, Comment, User
from reviews.validators import validate_username


# User = get_user_model()


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'bio', 'first_name', 'last_name', 'email', 'role',
        )


class NotAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)


class GetTokenSerializer(Serializer):
    username = CharField(
        required=True)
    confirmation_code = CharField(
        required=True)


class SignUpSerializer(Serializer):
    email = EmailField(
        required=True,
        max_length=254,)
    username = CharField(
        required=True,
        validators=[validate_username],
        max_length=150)

class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        lookup_field = 'slug'


class TitleGetSerializer(ModelSerializer):
    rating = IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
  
    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre','category',
        )
        model = Title


class TitleNotGetSerializer(ModelSerializer):
    genre = SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    # allow_null = True
    category = SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    def validate_year(self, value):
        year = datetime.date.today().year
        if (value >= year):
            raise ValidationError('Проверьте год!')
        return value

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre','category',
        )
        # read_only_fields = ('author',)
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
        read_only_fields = ('review', 'author',)
        
        
class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    score = IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        required=True,
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UsersSerializer(instance.author).data['username']
        return representation

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
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        model = Review
        read_only_fields = ('author', 'title',)
