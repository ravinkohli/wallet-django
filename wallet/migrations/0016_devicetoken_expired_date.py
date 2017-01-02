# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0015_devicetoken_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetoken',
            name='expired_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
