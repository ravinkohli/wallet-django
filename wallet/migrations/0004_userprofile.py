# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('wallet', '0003_auto_20161214_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('date_ob', models.DateField()),
                ('sex', models.CharField(max_length=1)),
                ('wallet_id', models.ForeignKey(to='wallet.Wallet')),
            ],
        ),
    ]
