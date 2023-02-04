from django.contrib.auth import get_user_model
import datetime

from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField, SlugRelatedField, ValidationError
)

from reviews.models import Category, Genre, Title

User = get_user_model()


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category
        lookup_field = 'slug'


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre
        lookup_field = 'slug'


class TitleGetSerializer(ModelSerializer):
    rating = SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
  
    def get_rating(self, obj):
        pass

    class Meta:
        fields = '__all__'
        model = Title


class TitleNotGetSerializer(ModelSerializer):
    rating = SerializerMethodField()
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

    def get_rating(self, obj):
        pass

    class Meta:
        fields = '__all__'
        model = Category
