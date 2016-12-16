# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wallet.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_name', models.CharField(max_length=15)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=15)),
                ('amount', models.IntegerField(validators=[wallet.models.validate_not_neg])),
            ],
            options={
                'permissions': (('add_money', 'can deposit money'), ('subtract_money', 'can take withdraw money')),
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet_id',
            field=models.ForeignKey(to='wallet.Wallet'),
        ),
    ]
