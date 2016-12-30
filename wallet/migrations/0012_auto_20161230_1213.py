# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0011_token_tokendevice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokendevice',
            name='token',
            field=models.OneToOneField(to='wallet.Token'),
        ),
    ]
