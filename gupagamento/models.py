from django.db import models
from djmoney.models.fields import MoneyField


class Contribuinte(models.Model):
    nome = models.CharField(max_length=250)
    nif = models.CharField(max_length=14, null=True, blank=True)
    morada = models.CharField(max_length=300)
    municipio = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.nome


class Taxa(models.Model):
    titulo = models.CharField(max_length=10, null=True, blank=True)
    valor_contrato = MoneyField(max_digits=10, decimal_places=2, default_currency="AOA")
    valor_pago = MoneyField(max_digits=10, decimal_places=2, default_currency="AOA")
    data_pagamento = models.DateField()
    contribuinte = models.ForeignKey(
        Contribuinte, on_delete=models.CASCADE, related_name="taxas_pagas"
    )

    def __str__(self) -> str:
        if self.titulo:
            return f"titulo: {self.titulo} contribuiente {self.contribuinte}"
        return self.id
