# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-09-17 19:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('retrospective', '0007_planning_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planning',
            name='user',
            field=models.ForeignKey(blank=True, default=15, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
