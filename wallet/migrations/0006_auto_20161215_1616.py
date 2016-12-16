# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_auto_20161215_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='username',
            field=models.CharField(default=b'', max_length=15),
        ),
    ]
