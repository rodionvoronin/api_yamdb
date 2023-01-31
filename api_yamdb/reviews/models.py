from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=200)

    
class Genre(models.Model):
    title = models.CharField(max_length=200)


class Title(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
        
    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title