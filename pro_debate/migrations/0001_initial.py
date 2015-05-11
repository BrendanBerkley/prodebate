# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elaboration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tree_relation', models.CharField(max_length=1, choices=[(b'G', b'General'), (b'S', b'Supporting Point'), (b'C', b'Counterpoint')])),
                ('elaboration', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manifestation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=400)),
                ('title', models.CharField(max_length=255)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position_statement', models.CharField(max_length=255)),
                ('elaboration', models.ForeignKey(blank=True, to='pro_debate.Elaboration', null=True)),
                ('manifestation', models.ForeignKey(blank=True, to='pro_debate.Manifestation', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
        migrations.AddField(
            model_name='elaboration',
            name='related_to',
            field=models.ForeignKey(related_name='position_tree_relation', blank=True, to='pro_debate.Position', null=True),
        ),
    ]
