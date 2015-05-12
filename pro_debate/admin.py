from django.contrib import admin

# Register your models here.
from .models import Position, Elaboration, Manifestation

admin.site.register(Elaboration)
admin.site.register(Manifestation)


class ElaborationInline(admin.TabularInline):
    model = Elaboration
    extra = 1
    fk_name = 'elaborates'

class ManifestationInline(admin.TabularInline):
    model = Manifestation
    extra = 0


class PositionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['position_statement', 'tags']}),
    ]
    inlines = [ElaborationInline, ManifestationInline]

admin.site.register(Position, PositionAdmin)