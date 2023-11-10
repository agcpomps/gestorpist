from django.db import models


class Especialidade(models.Model):
    nome = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        indexes = [
            models.Index(fields=['nome'])
        ]
        verbose_name = "especialidade"
        verbose_name_plural = "categorias"

    def __str__(self) -> str:
        return self.nome



class Empresa(models.Model):
    especialidade = models.ForeignKey(Especialidade, related_name="empresas", on_delete=models.CASCADE)
    nome = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200)
    gerente = models.CharField(max_length=250)
    telefone = models.CharField(max_length=9)
    email = models.EmailField()
    morada = models.CharField(max_length=250)
    provincia = models.CharField(max_length=200, verbose_name="província")
    municipio = models.CharField(max_length=200, verbose_name="município")
    nif = models.CharField(max_length=16)
    class Meta:
        indexes = [
            models.Index(fields=['nome'])
        ]

    def __str__(self) -> str:
        return self.nome

class Alvara(models.Model):
    numero = models.CharField(max_length=200)
    emissao = models.DateField()
    termino = models.DateField()
    tipo = models.IntegerField()
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE, related_name="alvara")

class Documento(models.Model):
    descricao = models.CharField(max_length=255, blank=True)
    documento = models.FileField(upload_to="documents")
    

    def __str__(self) -> str:
        return f"Alvara numero {self.numero} empresa {self.empresa}"


    
