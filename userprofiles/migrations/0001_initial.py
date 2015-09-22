# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('paquetes', '0001_initial'),
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
                ('email', models.EmailField(max_length=100, verbose_name=b'Email')),
                ('facebook', models.URLField(verbose_name=b'Facebook', blank=True)),
                ('twitter', models.URLField(verbose_name=b'Twitter', blank=True)),
                ('web', models.URLField(verbose_name=b'Web', blank=True)),
                ('codigoValidacion', models.CharField(max_length=100, verbose_name=b'Codigo validacion')),
                ('logo', django_resized.forms.ResizedImageField(upload_to=b'userprofiles/logos', null=True, verbose_name=b'Logo', blank=True)),
                ('cartel', models.ImageField(upload_to=b'userprofiles/carteles', null=True, verbose_name=b'Cartel', blank=True)),
                ('visitas', models.IntegerField(default=0, verbose_name=b'Visualizaciones del afiliado')),
            ],
        ),
        migrations.CreateModel(
            name='Giro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('giro', models.CharField(max_length=100, verbose_name=b'Giro o actividad de la empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_pago', models.DateTimeField(auto_now_add=True, verbose_name=b'Fecha de pago')),
                ('meses', models.PositiveIntegerField(default=1, verbose_name=b'Meses de pago')),
                ('status', models.BooleanField(default=True, verbose_name=b'Status del pago')),
                ('cantidad_pagada', models.FloatField(verbose_name=b'Cantidad pagada')),
                ('afiliado', models.ForeignKey(related_name='pagos', to='userprofiles.Afiliado')),
            ],
        ),
        migrations.AddField(
            model_name='afiliado',
            name='giros',
            field=models.ManyToManyField(related_name='afiliados', to='userprofiles.Giro'),
        ),
        migrations.AddField(
            model_name='afiliado',
            name='paquete',
            field=models.ForeignKey(related_name='afiliados', to='paquetes.Paquete'),
        ),
        migrations.AddField(
            model_name='afiliado',
            name='user',
            field=models.OneToOneField(related_name='perfil_afiliado', to=settings.AUTH_USER_MODEL),
        ),
    ]
