from django.db import models
from django.conf import settings


class Project(models.Model):
    """A project owned by a department within GPIST."""

    class Status(models.TextChoices):
        PLANEADO = "PL", "Planeado"
        EM_CURSO = "EC", "Em Curso"
        EM_PAUSA = "PA", "Em Pausa"
        CONCLUIDO = "CO", "Concluído"
        CANCELADO = "CA", "Cancelado"

    class Priority(models.TextChoices):
        BAIXA = "B", "Baixa"
        MEDIA = "M", "Média"
        ALTA = "A", "Alta"
        URGENTE = "U", "Urgente"

    name = models.CharField(max_length=200, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")
    department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.PROTECT,
        related_name="projects",
        verbose_name="Departamento",
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PLANEADO,
        verbose_name="Estado",
    )
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIA,
        verbose_name="Prioridade",
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_projects",
        verbose_name="Responsável",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="projects",
        verbose_name="Equipa",
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="Data de Início")
    end_date = models.DateField(null=True, blank=True, verbose_name="Prazo")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_projects",
        verbose_name="Criado por",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificado")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Projecto"
        verbose_name_plural = "Projectos"

    def __str__(self) -> str:
        return self.name

    @property
    def progress(self) -> int:
        """Percentage of tasks marked as concluded (0–100)."""
        total = self.tasks.count()
        if not total:
            return 0
        concluidas = self.tasks.filter(status=Task.Status.CONCLUIDA).count()
        return round(concluidas / total * 100)


class Task(models.Model):
    """A unit of work belonging to a project."""

    class Status(models.TextChoices):
        PENDENTE = "P", "Pendente"
        EM_CURSO = "C", "Em Curso"
        BLOQUEADA = "B", "Bloqueada"
        CONCLUIDA = "D", "Concluída"

    class Priority(models.TextChoices):
        BAIXA = "B", "Baixa"
        MEDIA = "M", "Média"
        ALTA = "A", "Alta"
        URGENTE = "U", "Urgente"

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Projecto",
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name="Atribuída a",
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDENTE,
        verbose_name="Estado",
    )
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIA,
        verbose_name="Prioridade",
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Prazo")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Concluída em")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modificada")

    class Meta:
        ordering = ["due_date", "created_at"]
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def __str__(self) -> str:
        return self.title


class ProjectComment(models.Model):
    """A comment/update on a project's activity feed."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Projecto",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_comments",
        verbose_name="Autor",
    )
    body = models.TextField(verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado")

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"

    def __str__(self) -> str:
        return f"{self.author} — {self.project}"
