# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariofinal',
            name='full_name',
            field=models.CharField(default='Sin nombre', max_length=250, verbose_name=b'Nombre Completo'),
            preserve_default=False,
        ),
    ]
