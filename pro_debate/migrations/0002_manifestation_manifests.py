# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pro_debate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manifestation',
            name='manifests',
            field=models.ForeignKey(default=1, to='pro_debate.Position'),
            preserve_default=False,
        ),
    ]
