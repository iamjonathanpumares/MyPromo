# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0002_auto_20150122_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afiliado',
            name='facebook',
            field=models.URLField(verbose_name=b'Facebook', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='afiliado',
            name='twitter',
            field=models.URLField(verbose_name=b'Twitter', blank=True),
            preserve_default=True,
        ),
    ]
