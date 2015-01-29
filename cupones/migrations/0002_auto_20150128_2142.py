# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupon',
            name='status',
            field=models.CharField(default=b'Activo', max_length=10),
            preserve_default=True,
        ),
    ]
