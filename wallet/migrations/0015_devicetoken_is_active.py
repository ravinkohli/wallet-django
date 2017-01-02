# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0014_auto_20161230_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetoken',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
