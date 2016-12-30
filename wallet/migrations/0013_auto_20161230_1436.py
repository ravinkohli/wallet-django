# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0012_auto_20161230_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokendevice',
            name='token',
        ),
        migrations.AddField(
            model_name='token',
            name='device_browser',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.DeleteModel(
            name='TokenDevice',
        ),
    ]
