# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0003_auto_20150206_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupon',
            name='fecha_inicio',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 6, 12, 18, 681586, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
