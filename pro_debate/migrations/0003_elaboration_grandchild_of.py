# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pro_debate', '0002_manifestation_manifests'),
    ]

    operations = [
        migrations.AddField(
            model_name='elaboration',
            name='grandchild_of',
            field=models.ForeignKey(related_name='grandchild_of_position', blank=True, to='pro_debate.Position', null=True),
        ),
    ]
