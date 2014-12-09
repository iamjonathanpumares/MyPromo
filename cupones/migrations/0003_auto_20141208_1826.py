# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0002_usuarioscupones_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuarioscupones',
            old_name='cupon',
            new_name='cupon_usuario',
        ),
    ]
