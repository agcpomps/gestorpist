from django.db import models
from django.contrib.auth.models import AbstractUser


class Department(models.Model):
    """Canonical organizational department, shared by all modules."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Nome")
    description = models.TextField(blank=True, verbose_name="Descrição")

    class Meta:
        ordering = ["name"]
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self) -> str:
        return self.name


class CustomUser(AbstractUser):
    departamento = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Departamento",
    )

    def __str__(self) -> str:
        return self.username

    def manages(self, department) -> bool:
        """True if this user can manage records belonging to `department`."""
        if self.is_staff or self.is_superuser:
            return True
        department_id = getattr(department, "id", department)
        return self.departamento_id is not None and self.departamento_id == department_id
