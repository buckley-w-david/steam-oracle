# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 09:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='profiles',
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_games',
            field=models.ManyToManyField(related_name='liked_games', to='recommend.Game'),
        ),
        migrations.AddField(
            model_name='profile',
            name='owned_games',
            field=models.ManyToManyField(related_name='owned_games', to='recommend.Game'),
        ),
    ]