# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0002_auto_20150128_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupon',
            name='imagen',
            field=models.ImageField(upload_to=b'cupones/imagenes', blank=True),
            preserve_default=True,
        ),
    ]
