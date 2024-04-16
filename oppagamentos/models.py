from django.db import models
from django.utils import timezone


class Classe(models.TextChoices):
    TERCEIRA = "3ª", "Terceira"
    QUARTA = "4ª", "Quarta"


class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    municipio = models.CharField(max_lebgth=200)
    classe = models.CharField(
        max_length=3, choices=Classe.choices, default=Classe.QUARTA
    )
    numero_de_telefone = models.CharField(max_length=30, null=True, Blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self) -> str:
        return self.nome


class TituloHabilitante(models.TextChoices):
    CONSTRUCAO = "CCOP", "Construção"
    FISCALIZACAO = "FO", "Fiscalização"


class Alvara(models.Model):
    numero_de_titilo = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    numero_ordem_pagamento = models.CharField(max_length=14)
    titulo_habilitante = models.CharField(
        max_length=4,
        choices=TituloHabilitante.choices,
        default=TituloHabilitante.CONSTRUCAO,
    )

    emissao = models.DateField()
    termino = models.DateField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    @classmethod
    def valor_total(cls):
        return cls.objects.aggregate(models.Sum("valor"))["valor__sum"]

    @property
    def total(self):
        return Alvara.valor_total()

    @property
    def esta_caducado(self):
        current_datetime = timezone.now()
        current_date = current_datetime.date()

        if current_date > self.termino:
            return True

        return False

    def __str__(self) -> str:
        return f"{self.empresa} - {self.numero_de_titilo}"
