# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wallet.models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_transaction_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.IntegerField(default=0, validators=[wallet.models.validate_not_neg]),
        ),
    ]
