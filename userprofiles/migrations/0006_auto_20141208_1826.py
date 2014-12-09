# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofiles', '0005_auto_20141207_2355'),
    ]

    operations = [
        migrations.CreateModel(
            name='Afiliado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreEmpresa', models.CharField(max_length=255, verbose_name=b'Empresa')),
                ('representante', models.CharField(max_length=200, verbose_name=b'Representante')),
                ('direccion', models.CharField(max_length=255, verbose_name=b'Direccion')),
                ('telefono', models.CharField(max_length=15, verbose_name=b'Telefono')),
                ('email', models.EmailField(max_length=100, verbose_name=b'Email')),
                ('facebook', models.CharField(max_length=200, verbose_name=b'Facebook')),
                ('twitter', models.CharField(max_length=100, verbose_name=b'Twitter')),
                ('codigoValidacion', models.CharField(max_length=255, verbose_name=b'Codigo validacion')),
                ('logo', models.ImageField(upload_to=b'logos', verbose_name=b'Logo')),
                ('giro', models.CharField(max_length=100, verbose_name=b'Giro')),
                ('cartel', models.ImageField(upload_to=b'carteles', verbose_name=b'Cartel')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='promotor',
            name='user',
        ),
        migrations.DeleteModel(
            name='Promotor',
        ),
        migrations.DeleteModel(
            name='UsuarioAfiliado',
        ),
    ]
