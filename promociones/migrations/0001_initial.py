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
            name='Promocion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=60)),
                ('fecha_creacion', models.DateField(auto_now=True)),
                ('vigencia', models.DateField()),
                ('descripcion', models.TextField()),
                ('status', models.CharField(max_length=10)),
                ('imagen', models.ImageField(upload_to=b'promociones/imagenes')),
                ('promocion_afiliado', models.ForeignKey(related_name='promociones', to='userprofiles.Afiliado')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsuariosPromociones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(auto_now=True)),
                ('promocion', models.ForeignKey(to='promociones.Promocion')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='promocion',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='promociones.UsuariosPromociones'),
            preserve_default=True,
        ),
    ]
