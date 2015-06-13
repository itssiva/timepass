# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_remove_image_thumbnail2'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='thumbnail2',
            field=models.ImageField(null=True, upload_to=b'images/', blank=True),
        ),
    ]
