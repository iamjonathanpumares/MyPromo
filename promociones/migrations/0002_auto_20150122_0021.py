# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promociones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocion',
            name='promocion_afiliado',
            field=models.ForeignKey(related_name='promociones', to='userprofiles.Afiliado'),
            preserve_default=True,
        ),
    ]
