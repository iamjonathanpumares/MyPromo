# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupon',
            name='cupon_afiliado',
            field=models.ForeignKey(related_name='cupones', to='userprofiles.Afiliado'),
            preserve_default=True,
        ),
    ]
