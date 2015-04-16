from django.contrib import admin

# Register your models here.
from .models import Point, Prompt, SupportingPoint, CounterPoint

admin.site.register(Prompt)
admin.site.register(Point)
admin.site.register(SupportingPoint)
admin.site.register(CounterPoint)