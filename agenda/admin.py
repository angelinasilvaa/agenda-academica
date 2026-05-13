from django.contrib import admin
from .models import Compromisso

@admin.register(Compromisso)
class CompromissoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_hora', 'tipo', 'concluido')
    list_filter = ('tipo', 'concluido')
    search_fields = ('titulo',)
