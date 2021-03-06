# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 07:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(20)])),
                ('content', models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(20)])),
                ('image_url', models.URLField()),
                ('send_at', models.DateTimeField(verbose_name='Send at')),
                ('user_query', models.TextField(verbose_name='User query')),
                ('is_sent', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'notification',
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
