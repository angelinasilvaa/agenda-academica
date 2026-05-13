from django.db import models

class Compromisso(models.Model):
    TIPO_CHOICES = [
        ('PROVA', 'Prova'),
        ('TRABALHO', 'Trabalho'),
        ('ATENDIMENTO', 'Atendimento com Professor'),
    ]

    titulo = models.CharField(max_length=150, verbose_name="Título")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PROVA')
    concluido = models.BooleanField(default=False, verbose_name="Concluído")

    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"

    class Meta:
        verbose_name = "Compromisso"
        verbose_name_plural = "Compromissos"

# Create your models here.
