# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(related_name='perfil_promotor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('puntuacion', models.FloatField(verbose_name=b'Puntuaci\xc3\xb3n de cada usuario')),
                ('afiliado', models.ForeignKey(to='userprofiles.Afiliado')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioFinal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=250, verbose_name=b'Nombre Completo')),
                ('afiliados', models.ManyToManyField(related_name='usuarios_finales', through='userprofiles.Rating', to='userprofiles.Afiliado')),
                ('user', models.OneToOneField(related_name='perfil_usuariofinal', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='usuario_final',
            field=models.ForeignKey(to='userprofiles.UsuarioFinal'),
        ),
    ]
