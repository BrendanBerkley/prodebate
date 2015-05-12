from django.db import models

from taggit.managers import TaggableManager


class Position(models.Model):
    position_statement = models.CharField(max_length=255)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.position_statement

class Elaboration(models.Model):
    TREE_RELATION_CHOICES = (
        ('G', 'General'),
        ('S', 'Supporting Point'),
        ('C', 'Counterpoint'),
    )

    tree_relation = models.CharField(
        max_length=1, 
        choices=TREE_RELATION_CHOICES
    )
    elaborates = models.ForeignKey(
        'Position', 
        blank=True, 
        null=True,
        related_name='elaboration_of_position',
    )
    child_of = models.ForeignKey(
        'Position', 
        blank=True, 
        null=True,
        related_name='child_of_position',
    )
    elaboration = models.TextField(blank=True)

    def __unicode__(self):
        return self.elaborates.position_statement + " (" + \
            self.tree_relation + ")"

class Manifestation(models.Model):
    url = models.URLField(max_length=400)
    title = models.CharField(max_length=255)
    manifests = models.ForeignKey('Position')
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.title
