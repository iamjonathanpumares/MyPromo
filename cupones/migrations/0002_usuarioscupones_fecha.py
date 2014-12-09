# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cupones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioscupones',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2014, 12, 8, 23, 50, 38, 161448, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
