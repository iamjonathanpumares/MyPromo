# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0002_usuariofinal_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='afiliado',
            name='web',
            field=models.URLField(verbose_name=b'Web', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='afiliado',
            name='codigoValidacion',
            field=models.CharField(max_length=100, verbose_name=b'Codigo validacion'),
            preserve_default=True,
        ),
    ]
