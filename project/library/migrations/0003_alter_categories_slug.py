# Generated by Django 4.0.3 on 2022-05-04 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_categories_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(max_length=255, null=True),
        ),
    ]