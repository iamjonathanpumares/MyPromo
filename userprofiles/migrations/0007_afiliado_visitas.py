# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0006_giro'),
    ]

    operations = [
        migrations.AddField(
            model_name='afiliado',
            name='visitas',
            field=models.IntegerField(default=0, verbose_name=b'Visualizaciones del afiliado'),
            preserve_default=True,
        ),
    ]
