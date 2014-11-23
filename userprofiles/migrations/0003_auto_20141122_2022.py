# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0002_usuarioafiliado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='cartel',
            field=models.ImageField(upload_to=b'carteles', verbose_name=b'Cartel'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='codigoValidacion',
            field=models.CharField(max_length=255, verbose_name=b'Codigo validacion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='direccion',
            field=models.CharField(max_length=255, verbose_name=b'Direccion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='email',
            field=models.EmailField(max_length=100, verbose_name=b'Email'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='facebook',
            field=models.CharField(max_length=200, verbose_name=b'Facebook'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='giro',
            field=models.CharField(max_length=100, verbose_name=b'Giro'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='logo',
            field=models.ImageField(upload_to=b'logos', verbose_name=b'Logo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='nombreEmpresa',
            field=models.CharField(max_length=255, verbose_name=b'Empresa'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='representante',
            field=models.CharField(max_length=200, verbose_name=b'Representante'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='telefono',
            field=models.CharField(max_length=15, verbose_name=b'Telefono'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='twitter',
            field=models.CharField(max_length=100, verbose_name=b'Twitter'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuarioafiliado',
            name='username',
            field=models.CharField(unique=True, max_length=100, verbose_name=b'Usuario'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariopromotor',
            name='apellidos',
            field=models.CharField(max_length=200, verbose_name=b'Apellidos'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariopromotor',
            name='nombre',
            field=models.CharField(max_length=200, verbose_name=b'Nombre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariopromotor',
            name='username',
            field=models.CharField(unique=True, max_length=100, verbose_name=b'Usuario'),
            preserve_default=True,
        ),
    ]
