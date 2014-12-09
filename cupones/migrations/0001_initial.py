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
                ('vigencia', models.DateField()),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(upload_to=b'cupones/imagenes')),
                ('cupon_afiliado', models.ForeignKey(to='userprofiles.Afiliado')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuariosCupones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=10)),
                ('fecha', models.DateField()),
                ('cupon_usuario', models.ForeignKey(to='cupones.Cupon')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cupon',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='cupones.UsuariosCupones'),
            preserve_default=True,
        ),
    ]
