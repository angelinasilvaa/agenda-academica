from django.contrib import admin
from .models import Compromisso

@admin.register(Compromisso)
class CompromissoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'data_hora', 'tipo', 'concluido')
    list_filter = ('tipo', 'concluido', 'usuario')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_hora'

    # Liga automaticamente o compromisso ao utilizador do painel admin ao salvar
    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

