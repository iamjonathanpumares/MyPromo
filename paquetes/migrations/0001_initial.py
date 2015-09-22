# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paquete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_paquete', models.CharField(max_length=50, verbose_name=b'Nombre del paquete')),
                ('mensualidad', models.FloatField(verbose_name=b'Mensualidad')),
                ('max_locales', models.PositiveSmallIntegerField(verbose_name=b'M\xc3\xa1ximo de locales por afiliado')),
                ('max_promo', models.PositiveSmallIntegerField(verbose_name=b'M\xc3\xa1ximo de promociones por afiliado')),
                ('max_cupones', models.PositiveSmallIntegerField(verbose_name=b'M\xc3\xa1ximo de cupones por afiliado')),
                ('have_fidelidad', models.BooleanField(verbose_name=b'Tiene fidelidad')),
            ],
        ),
    ]
