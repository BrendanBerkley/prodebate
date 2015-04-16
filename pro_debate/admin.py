from django.contrib import admin

# Register your models here.
from .models import Point, Prompt

admin.site.register(Prompt)
admin.site.register(Point)