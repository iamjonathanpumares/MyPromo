# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0007_afiliado_visitas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='afiliado',
            name='giro',
        ),
        migrations.AddField(
            model_name='afiliado',
            name='giros',
            field=models.ManyToManyField(related_name='afiliados', to='userprofiles.Giro'),
            preserve_default=True,
        ),
    ]
