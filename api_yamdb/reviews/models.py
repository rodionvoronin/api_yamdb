# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_username

# User = get_user_model()

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
USER_RU = 'юзер'
MODERATOR_RU = 'модератор'
ADMIN_RU = 'админ'
ROLES = (
    (USER, USER_RU),
    (MODERATOR, MODERATOR_RU),
    (ADMIN, ADMIN_RU),
)


class User(AbstractUser):
    username = models.CharField(validators=(validate_username,),
                                max_length=150,
                                unique=True,
                                blank=False,
                                null=False,)
    email = models.EmailField(verbose_name='E-Mail',
                              unique=True,
                              max_length=254,
                              blank=False,
                              null=False,)
    bio = models.TextField(verbose_name="О себе",
                           blank=True,
                           null=True,
                           max_length=300,)
    first_name = models.CharField('имя',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField('фамилия',
                                 max_length=150,
                                 blank=True)
    role = models.CharField(verbose_name='Уровень доступа',
                            choices=ROLES,
                            default=USER,
                            max_length=50)

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


    class Meta:
        ordering = ('slug', )
    
    def __str__(self):
        return self.name

    
class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


    class Meta:
        ordering = ('slug', )
    
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
    )     
        
    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
