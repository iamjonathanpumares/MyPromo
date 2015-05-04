# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promociones', '0004_promocion_fecha_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariospromociones',
            name='fecha',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
