# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioAfiliado',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('idUsuarioAfiliado', models.IntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=100, verbose_name=b'username')),
                ('nombreEmpresa', models.CharField(max_length=255)),
                ('representante', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=100)),
                ('facebook', models.CharField(max_length=200)),
                ('twitter', models.CharField(max_length=100)),
                ('codigoValidacion', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to=b'logos')),
                ('giro', models.CharField(max_length=100)),
                ('cartel', models.ImageField(upload_to=b'carteles')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
