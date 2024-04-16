import os
from django.db import models


class Empresa(models.Model):

    class Especialidade(models.TextChoices):
        CONSTRUCAO = "CT", "Construção"
        FISCALIZACAO = "FI", "Fiscalização"
        PROJECTO = "PJ", "Projecto"

    nome = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200)
    gerente = models.CharField(max_length=250, blank=True, null=True)
    telefone = models.CharField(max_length=9)
    email = models.EmailField(blank=True, null=True)
    morada = models.CharField(max_length=250)
    provincia = models.CharField(max_length=200, verbose_name="província")
    municipio = models.CharField(max_length=200, verbose_name="município")
    nif = models.CharField(max_length=16, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    especialidade = models.CharField(
        max_length=2, choices=Especialidade.choices, default=Especialidade.CONSTRUCAO
    )

    class Meta:
        indexes = [models.Index(fields=["nome"])]

    def __str__(self) -> str:
        return self.nome


class Alvara(models.Model):
    numero = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    emissao = models.DateField()
    termino = models.DateField()
    tipo = models.IntegerField()
    empresa = models.OneToOneField(
        Empresa, on_delete=models.CASCADE, related_name="alvara"
    )

    def __str__(self) -> str:
        return f"{self.numero} | {self.empresa}"


class Documento(models.Model):
    descricao = models.CharField(max_length=255, blank=True)
    documento = models.FileField(upload_to="documentos/", blank=True, null=True)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name="documentos"
    )

    def __str__(self) -> str:
        return f"Alvara numero {self.documento} empresa {self.empresa}"

    def save(self, *args, **kwargs):
        if not self.documento:
            return
        upload_to = os.path.join("documentos/", self.empresa.nome)

        self.documento.field.upload_to = upload_to

        super(Documento, self).save(*args, *kwargs)
