# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-15 00:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_task_parent_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='parent_list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='lists.List'),
        ),
    ]
