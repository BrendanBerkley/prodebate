from django.db import models

from taggit.managers import TaggableManager

# class Category(models.Model):
#     MEGA_CATEGORIES = (
#         ('P', 'Politics'),
#         ('S', 'Sports'),
#         ('R', 'Religion'),
#         ('M', 'Movies'),
#     )
#     name = models.CharField(max_length=255)
#     mega_category = models.CharField(max_length=1, choices=MEGA_CATEGORIES)

#     def __unicode__(self):
#         return self.name

class Point(models.Model):
    thesis = models.CharField(max_length=255)
    thesis_elaborated = models.TextField(blank=True)
    # category = models.ForeignKey(Category)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.thesis

class Prompt(models.Model):
    prompt = models.CharField(max_length=255)
    points = models.ManyToManyField(Point, blank=True)
    # category = models.ForeignKey(Category)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.prompt