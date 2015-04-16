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
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thesis', models.CharField(max_length=255)),
                ('thesis_elaborated', models.TextField(blank=True)),
                ('citation', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prompt', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CounterPoint',
            fields=[
                ('point_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pro_debate.Point')),
            ],
            bases=('pro_debate.point',),
        ),
        migrations.CreateModel(
            name='SupportingPoint',
            fields=[
                ('point_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pro_debate.Point')),
            ],
            bases=('pro_debate.point',),
        ),
        migrations.AddField(
            model_name='prompt',
            name='points',
            field=models.ManyToManyField(to='pro_debate.Point', blank=True),
        ),
        migrations.AddField(
            model_name='prompt',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='point',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='supportingpoint',
            name='point_supports',
            field=models.ForeignKey(related_name='points_this_supports', to='pro_debate.Point'),
        ),
        migrations.AddField(
            model_name='counterpoint',
            name='point_counters',
            field=models.ForeignKey(related_name='points_this_counters', to='pro_debate.Point'),
        ),
    ]
