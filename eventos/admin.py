from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "privado", "organizador")
    list_filter = ("privado", "tipo")
    search_fields = ("titulo", "descripcion")
