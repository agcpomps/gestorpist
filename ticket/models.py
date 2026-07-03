from django.db import models
from django.conf import settings


class Ticket(models.Model):
    class Priority(models.TextChoices):
        BAIXA = "B", "Baixa"
        MEDIA = "M", "Media"
        ALTA = "A", "Alta"
        URGENTE = "U", "Urgente"

    class Status(models.TextChoices):
        ABERTO = "A", "Aberto"
        EN_PROGRESSO = "P", "Em Progresso"
        RESOLVIDO = "R", "Resolvido"
        FECHADO = "F", "Fechado"

    title = models.CharField(max_length=200, verbose_name="Titulo")
    description = models.TextField(verbose_name="Descrição")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_tickets",
        verbose_name="Usuário",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )
    department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.CASCADE,
        related_name="department_tickets",
        verbose_name="Departamento",
    )
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIA,
        verbose_name="Prioridade",
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.ABERTO,
        verbose_name="Estado",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Ticket",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_comments",
        verbose_name="Autor",
    )
    body = models.TextField(verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.author} — {self.ticket}"
