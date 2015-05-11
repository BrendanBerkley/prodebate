from django.db import models

from taggit.managers import TaggableManager


class Position(models.Model):
    position_statement = models.CharField(max_length=255)
    elaboration = models.ForeignKey('Elaboration', blank=True, null=True)
    manifestation = models.ForeignKey('Manifestation', blank=True, null=True)
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
    related_to = models.ForeignKey(
        'Position', 
        blank=True, 
        null=True,
        related_name='position_tree_relation'
    )
    elaboration = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)

class Manifestation(models.Model):
    url = models.URLField(max_length=400)
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __unicode__(self):
        return self.title
