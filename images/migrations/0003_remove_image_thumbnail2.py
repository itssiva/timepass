# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_image_thumbnail2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='thumbnail2',
        ),
    ]
