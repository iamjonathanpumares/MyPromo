# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('direccion', models.CharField(max_length=80)),
                ('local_afiliado', models.ForeignKey(to='userprofiles.Afiliado')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
