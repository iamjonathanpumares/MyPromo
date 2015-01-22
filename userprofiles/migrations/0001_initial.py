# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Afiliado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreEmpresa', models.CharField(max_length=255, verbose_name=b'Empresa')),
                ('representante', models.CharField(max_length=200, verbose_name=b'Representante')),
                ('descripcion', models.TextField()),
                ('direccion', models.CharField(max_length=255, verbose_name=b'Direccion')),
                ('telefono', models.CharField(max_length=15, verbose_name=b'Telefono')),
                ('email', models.EmailField(max_length=100, verbose_name=b'Email')),
                ('facebook', models.CharField(max_length=200, verbose_name=b'Facebook')),
                ('twitter', models.CharField(max_length=100, verbose_name=b'Twitter')),
                ('codigoValidacion', models.CharField(max_length=255, verbose_name=b'Codigo validacion')),
                ('logo', django_resized.forms.ResizedImageField(upload_to=b'userprofiles/logos', verbose_name=b'Logo')),
                ('giro', models.CharField(max_length=100, verbose_name=b'Giro')),
                ('cartel', models.ImageField(upload_to=b'userprofiles/carteles', verbose_name=b'Cartel')),
                ('user', models.OneToOneField(related_name='perfil_afiliado', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Promotor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='perfil_promotor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuarioFinal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='perfil_usuariofinal', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
