# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='local',
            name='local_afiliado',
            field=models.ForeignKey(related_name='locales', to='userprofiles.Afiliado'),
            preserve_default=True,
        ),
    ]
