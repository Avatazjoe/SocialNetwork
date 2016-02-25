# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 20:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0003_entry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='photot',
            new_name='photo',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='id',
        ),
        migrations.AlterField(
            model_name='entry',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]