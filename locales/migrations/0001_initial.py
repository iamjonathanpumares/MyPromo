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
                ('direccion', models.CharField(max_length=150)),
                ('telefono', models.CharField(max_length=15, verbose_name=b'Telefono')),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('estado', models.CharField(max_length=150, verbose_name=b'Estado')),
                ('localidad', models.CharField(max_length=150, verbose_name=b'Localidad')),
                ('is_matriz', models.BooleanField()),
                ('imagen_local', models.ImageField(upload_to=b'userprofiles/locales', null=True, verbose_name=b'Imagen del local', blank=True)),
                ('afiliado', models.ForeignKey(related_name='locales', to='userprofiles.Afiliado')),
            ],
        ),
    ]
