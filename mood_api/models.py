from django.db import models
from django.contrib.auth.models import User


class DefaultMood(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nome do Humor")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    image = models.ImageField(
        upload_to="mood_images/", blank=True, null=True, verbose_name="Imagem do Humor"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Humor Padrão"
        verbose_name_plural = "Humores Padrão"
        ordering = ["name"]


class MoodEntry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="mood_entries",
        verbose_name="Usuário",
    )
    mood = models.ForeignKey(
        DefaultMood,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Humor Selecionado",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Descrição Adicional"
    )
    entry_date = models.DateField(verbose_name="Data da Entrada")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    def __str__(self):
        mood_name = self.mood.name if self.mood else "N/A"
        return f"{self.user.username} - {mood_name} em {self.entry_date.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Entrada de Humor"
        verbose_name_plural = "Entradas de Humor"
        unique_together = ("user", "entry_date")
        ordering = ["-entry_date", "-created_at"]
