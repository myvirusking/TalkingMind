# Generated by Django 2.1.3 on 2020-04-25 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200425_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='article_category',
            field=models.ManyToManyField(to='users.ArticleCategory'),
        ),
    ]