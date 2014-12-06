# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0003_auto_20141122_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariopromotor',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariopromotor',
            name='username',
            field=models.CharField(unique=True, max_length=25, verbose_name=b'Usuario'),
            preserve_default=True,
        ),
    ]
