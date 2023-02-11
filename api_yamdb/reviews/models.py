from django.contrib.auth.models import AbstractUser
# from django.contrib.auth import get_user_model
# from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from .validators import validate_username

# User = get_user_model()
USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

USER_ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=USER_ROLES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=255,
        blank=True,
    )

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


"""
@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()
"""


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('slug', )
        verbose_name = "Катигория"
        verbose_name_plural = "Катигории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ('slug', )
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

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

    class Meta:
        ordering = ('name', )
        verbose_name = "Подпись"
        verbose_name_plural = "Подписи"

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True,
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )

    def __str__(self):
        return self.text

    class Meta(object):
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='review'
            )
        ]


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
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta(object):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
