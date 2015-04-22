# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0005_auto_20150418_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Giro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('giro', models.CharField(max_length=100, verbose_name=b'Giro o actividad de la empresa')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
