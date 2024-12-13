from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Documento(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('RG', 'RG'),
        ('CNH', 'CNH'),
        ('PASSAPORTE', 'Passaporte'),
        ('COMPROVANTE_RESIDENCIA', 'Comprovante de Residência'),
        ('CONTRATO_SOCIAL', 'Contrato Social'),
    ]

    arrematante = models.ForeignKey(
        'Arrematante', related_name='documentos', on_delete=models.CASCADE, null=True, blank=True
    )
    vendedor = models.ForeignKey(
        'Vendedor', related_name='documentos', on_delete=models.CASCADE, null=True, blank=True
    )
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    documento = models.FileField(upload_to='documentos/', blank=False, null=False)
    data_upload = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Exemplo: Verificar o tamanho máximo do arquivo (10 MB)
        max_file_size = 10 * 1024 * 1024
        if self.documento and self.documento.size > max_file_size:
            raise ValidationError("O tamanho do arquivo não pode exceder 10 MB.")
        # Exemplo: Verificar extensões permitidas
        valid_extensions = ['.pdf', '.jpg', '.png']
        if self.documento and not any(self.documento.name.endswith(ext) for ext in valid_extensions):
            raise ValidationError(f"Permitido apenas arquivos: {', '.join(valid_extensions)}")

    def __str__(self):
        return f"{self.get_tipo_documento_display()} - {self.arrematante.user.username if self.arrematante else self.vendedor.user.username}"

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"



class Arrematante(models.Model):
    TIPO_CADASTRO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='arrematante')
    cpf_cnpj = models.CharField(max_length=30)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    telefone_comercial = models.CharField(max_length=15, blank=True, null=True)
    telefone_celular = models.CharField(max_length=15)

    tipo_cadastro = models.CharField(
        max_length=2,
        choices=TIPO_CADASTRO_CHOICES,
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_cadastro_display()}"


class Vendedor(models.Model):
    TIPO_CADASTRO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendedor")
    tipo_cadastro = models.CharField(max_length=2, choices=TIPO_CADASTRO_CHOICES, verbose_name="Tipo de Cadastro")
    cpf_cnpj = models.CharField(max_length=18, verbose_name="CPF/CNPJ")
    logradouro = models.CharField(max_length=255, verbose_name="Logradouro")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=255, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=50, verbose_name="Estado")
    cep = models.CharField(max_length=9, verbose_name="CEP")
    pais = models.CharField(max_length=50, verbose_name="País")
    telefone_comercial = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone Comercial")

    tipo_cadastro = models.CharField(
        max_length=2,
        choices=TIPO_CADASTRO_CHOICES,
        default='PF',
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_cadastro_display()}"


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")
    setor = models.CharField(max_length=100, verbose_name="Setor")
    telefone = models.CharField(max_length=15, verbose_name="Telefone de Contato")

    def __str__(self):
        return f"Admin: {self.user.username}"


# Sinais para criar perfis automaticamente após a criação de um usuário
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Determine aqui qual tipo de perfil criar, baseado em lógica de negócios
        pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "arrematante"):
        instance.arrematante.save()
    elif hasattr(instance, "vendedor"):
        instance.vendedor.save()
    elif hasattr(instance, "admin"):
        instance.admin.save()
