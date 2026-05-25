from django.db import models
from django.contrib.auth.models import User # <-- Importa o modelo User do Django

class Compromisso(models.Model):
    # Relaciona o compromisso diretamente ao utilizador que o criou
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilizador", null=True, blank=True)
    
    TIPO_CHOICES = [
        ('PROVA', 'Prova'),
        ('TRABALHO', 'Trabalho'),
        ('ATIVIDADE', 'Atividade'),
        ('ATENDIMENTO', 'Atendimento com Professor'),
        ('REPOSICAO', 'Reposição de Aula'),
        ('EVENTO', 'Evento / Visita Técnica'),
    ]

    titulo = models.CharField(max_length=150, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição/Local")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PROVA')
    concluido = models.BooleanField(default=False, verbose_name="Concluído")
    destacar = models.BooleanField(default=True, verbose_name="Exibir no Painel")

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = "Compromisso"
        verbose_name_plural = "Compromissos"
        ordering = ['data_hora']
