from django.db import models


class Contribuinte(models.Model):
    nome = models.CharField(max_length=200)
    nif = models.CharField(max_length=10, unique=True)
    morada = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=13, null=True, blank=True)

    def __str__(self) -> str:
        return self.nome


class Benificiario(models.Model):
    nome = models.CharField(max_length=200, default="GPIST")

    def __str__(self) -> str:
        return self.nome


class Distincao(models.TextChoices):
    PT = "PT"
    GG = "GG"


class Licenca(models.Model):
    numero = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()
    contribuinte = models.ForeignKey(
        Contribuinte, on_delete=models.CASCADE, related_name="licencas_pagas"
    )
    benificiario = models.ForeignKey(
        Benificiario, on_delete=models.CASCADE, related_name="licencas_recebidas"
    )
    potencia = models.FloatField(null=True, blank=True)
    distincao = models.CharField(max_length=2, choices=Distincao.choices)

    def __str__(self) -> str:
        return f"Licença nº {self.numero} contribuiente {self.contribuinte}"
