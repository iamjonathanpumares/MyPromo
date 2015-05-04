# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0004_cupon_fecha_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioscupones',
            name='fecha',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
