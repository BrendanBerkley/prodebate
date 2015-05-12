from django.contrib import admin

# Register your models here.
from .models import Position, Elaboration, Manifestation

# admin.site.register(Position)
admin.site.register(Elaboration)
admin.site.register(Manifestation)


class ElaborationInline(admin.TabularInline):
    model = Elaboration
    extra = 1
    fk_name = 'elaborates'


# class PositionInline(admin.TabularInline):
#     model = Position.child_positions.position_children
#     inlines = [ElaborationInline]
#     extra = 1

# class ManifestationInline(admin.TabularInline):
#     model = Manifestation


class PositionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['position_statement', 'tags']}),
    ]
    inlines = [ElaborationInline]
    # inlines = [PositionInline]

admin.site.register(Position, PositionAdmin)