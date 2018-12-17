# Generated by Django 2.1.2 on 2018-12-16 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tnd_api', '0003_rating_is_classic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='is_classic',
        ),
        migrations.AddField(
            model_name='rating',
            name='review_type',
            field=models.CharField(choices=[('normal', 'normal'), ('classic', 'classic'), ('not good', 'NOTGOOD')], default='normal', max_length=10),
        ),
    ]
