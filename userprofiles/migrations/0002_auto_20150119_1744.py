# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('userprofiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afiliado',
            name='logo',
            field=django_resized.forms.ResizedImageField(upload_to=b'userprofiles/logos', verbose_name=b'Logo'),
            preserve_default=True,
        ),
    ]
