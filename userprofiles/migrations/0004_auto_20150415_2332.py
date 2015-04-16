# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0003_auto_20150415_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='afiliado',
            name='num_votos',
            field=models.IntegerField(default=0, verbose_name=b'N\xc3\xbamero de votos'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='afiliado',
            name='votos_totales',
            field=models.FloatField(default=0, verbose_name=b'Votos totales'),
            preserve_default=True,
        ),
    ]
