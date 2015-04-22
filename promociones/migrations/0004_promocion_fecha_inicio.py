# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('promociones', '0003_auto_20150206_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='promocion',
            name='fecha_inicio',
            field=models.DateField(default=datetime.datetime(2015, 4, 22, 6, 22, 46, 833035, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
