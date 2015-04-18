# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0004_auto_20150415_2332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('puntuacion', models.FloatField(verbose_name=b'Puntuaci\xc3\xb3n de cada usuario')),
                ('afiliado', models.ForeignKey(to='userprofiles.Afiliado')),
                ('usuario_final', models.ForeignKey(to='userprofiles.UsuarioFinal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='afiliado',
            name='num_votos',
        ),
        migrations.RemoveField(
            model_name='afiliado',
            name='votos_totales',
        ),
        migrations.AddField(
            model_name='usuariofinal',
            name='afiliados',
            field=models.ManyToManyField(related_name='usuarios_finales', through='userprofiles.Rating', to='userprofiles.Afiliado'),
            preserve_default=True,
        ),
    ]
