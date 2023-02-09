# from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework.serializers import (
    CharField, ModelSerializer, SlugRelatedField, 
    ValidationError, PrimaryKeyRelatedField, IntegerField, 
    CharField,
)
from django.core.validators import MaxValueValidator, MinValueValidator
# from rest_framework.validators import UniqueTogetherValidator

import datetime

from reviews.models import Category, Genre, Title, Review, Comment, User
from reviews.validators import validate_username



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
  
    def get_rating(self, obj):
        pass

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
        read_only_fields = ('title', 'author',)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class AdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class TokenSerializer(ModelSerializer):
    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')
