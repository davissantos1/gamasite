# user_management/models.py
from django.db import models

class Cliente(models.Model):
    NOME_MAX_LENGTH = 100
    SOBRENOME_MAX_LENGTH = 100
    EMAIL_MAX_LENGTH = 254
    CPF_CNPJ_MAX_LENGTH = 18
    CEP_MAX_LENGTH = 9
    LOGRADOURO_MAX_LENGTH = 255
    COMPLEMENTO_MAX_LENGTH = 255
    BAIRRO_MAX_LENGTH = 100
    CIDADE_MAX_LENGTH = 100
    ESTADO_MAX_LENGTH = 50
    PAIS_MAX_LENGTH = 50
    TELEFONE_MAX_LENGTH = 15

    nome = models.CharField(max_length=NOME_MAX_LENGTH)
    sobrenome = models.CharField(max_length=SOBRENOME_MAX_LENGTH)
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    cpf_cnpj = models.CharField(max_length=CPF_CNPJ_MAX_LENGTH, unique=True)
    cep = models.CharField(max_length=CEP_MAX_LENGTH)
    logradouro = models.CharField(max_length=LOGRADOURO_MAX_LENGTH)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=COMPLEMENTO_MAX_LENGTH, blank=True, null=True)
    bairro = models.CharField(max_length=BAIRRO_MAX_LENGTH)
    cidade = models.CharField(max_length=CIDADE_MAX_LENGTH)
    estado = models.CharField(max_length=ESTADO_MAX_LENGTH)
    pais = models.CharField(max_length=PAIS_MAX_LENGTH)
    telefone_comercial = models.CharField(max_length=TELEFONE_MAX_LENGTH, blank=True, null=True)
    telefone_celular = models.CharField(max_length=TELEFONE_MAX_LENGTH)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
