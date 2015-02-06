# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promociones', '0002_auto_20150128_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocion',
            name='imagen',
            field=models.ImageField(upload_to=b'promociones/imagenes', blank=True),
            preserve_default=True,
        ),
    ]
