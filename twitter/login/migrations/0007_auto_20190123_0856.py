# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-23 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20190123_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitcomment',
            name='CommnetBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserProfile'),
        ),
    ]
