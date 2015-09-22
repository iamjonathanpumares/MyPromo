# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cupon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=40)),
                ('fecha_creacion', models.DateField(auto_now=True)),
                ('fecha_inicio', models.DateField()),
                ('vigencia', models.DateField()),
                ('descripcion', models.TextField()),
                ('status', models.CharField(default=b'Activo', max_length=10)),
                ('imagen', models.ImageField(upload_to=b'cupones/imagenes', blank=True)),
                ('cupon_afiliado', models.ForeignKey(related_name='cupones', to='userprofiles.Afiliado')),
            ],
        ),
        migrations.CreateModel(
            name='UsuariosCupones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('cupon_usuario', models.ForeignKey(to='cupones.Cupon')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cupon',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='cupones.UsuariosCupones'),
        ),
    ]
