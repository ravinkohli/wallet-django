# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0013_auto_20161230_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceToken',
            fields=[
                ('key', models.CharField(max_length=40, serialize=False, verbose_name='Key', primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('device_browser', models.CharField(max_length=25, null=True)),
                ('user', models.ForeignKey(related_name='devicetoken_auth_token', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
        ),
        migrations.RemoveField(
            model_name='token',
            name='user',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
    ]
