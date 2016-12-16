# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_auto_20161215_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='to',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
