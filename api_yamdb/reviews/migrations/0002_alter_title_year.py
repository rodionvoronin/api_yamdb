# Generated by Django 3.2 on 2023-02-12 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveBigIntegerField(db_index=True),
        ),
    ]
