from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

# Adicione constantes para tipos de usuário
USER_TYPE_CHOICES = [
    ('arrematante', 'Arrematante'),
    ('admin', 'Admin'),
    ('default', 'Default'),
]

# Adicione o campo ao modelo User
User.add_to_class('user_type', models.CharField(
    max_length=15, choices=USER_TYPE_CHOICES, default='default'
))

class Documento(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('RG', 'RG'),
        ('CNH', 'CNH'),
        ('PASSAPORTE', 'Passaporte'),
        ('COMPROVANTE_RESIDENCIA', 'Comprovante de Residência'),
        ('CONTRATO_SOCIAL', 'Contrato Social'),
        ('SELFIE', 'Selfie'),  
    ]

    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('A', 'Aprovado'),
        ('R', 'Rejeitado'),
    ]

    arrematante = models.ForeignKey(
        'Arrematante', related_name='documentos', on_delete=models.CASCADE, null=True, blank=True
    )
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    documento = models.FileField(upload_to='documentos/', storage=FileSystemStorage(location=settings.PROTECTED_DOCUMENTS_DIR), blank=False, null=False)
    data_upload = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')  # Campo de status

    def clean(self):
        # Verificar o tamanho máximo do arquivo (10 MB)
        max_file_size = 10 * 1024 * 1024
        if self.documento and self.documento.size > max_file_size:
            raise ValidationError("O tamanho do arquivo não pode exceder 10 MB.")
        
        # Verificar extensões permitidas
        valid_extensions = ['.pdf', '.jpg', '.png']
        if self.documento and not any(self.documento.name.endswith(ext) for ext in valid_extensions):
            raise ValidationError(f"Permitido apenas arquivos: {', '.join(valid_extensions)}")

    def clean_user_document(self):
        # Validar qual tipo de usuário está enviando o documento e garantir que os documentos sejam válidos
        if self.arrematante:
            if self.arrematante.tipo_cadastro == 'PF':
                if self.tipo_documento == 'COMPROVANTE_RESIDENCIA':
                    return  # Comprovante de Residência é permitido para PF
                elif self.tipo_documento not in ['RG', 'CNH', 'PASSAPORTE', 'SELFIE']:
                    raise ValidationError('Para Pessoa Física (PF), é necessário enviar RG, CNH, Passaporte, Comprovante de Residência ou Selfie.')
            elif self.arrematante.tipo_cadastro == 'PJ':
                if self.tipo_documento in ['COMPROVANTE_RESIDENCIA', 'CONTRATO_SOCIAL', 'SELFIE']:
                    return  # Comprovante de Residência, Contrato Social e Selfie são permitidos para PJ
                raise ValidationError('Para Pessoa Jurídica (PJ), é necessário enviar Contrato Social, Comprovante de Residência ou Selfie.')

    def save(self, *args, **kwargs):
        self.clean_user_document()  # Chama a validação do documento antes de salvar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_tipo_documento_display()} - {self.arrematante.user.username}"

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

    class Meta:
        verbose_name = "Arrematante"
        verbose_name_plural = "Arrematantes"


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")
    setor = models.CharField(max_length=100, verbose_name="Setor")
    telefone = models.CharField(max_length=15, verbose_name="Telefone de Contato")

    def __str__(self):
        return f"Admin: {self.user.username}"

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"



# Sinal para criar perfis automaticamente após a criação de um usuário
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Criar perfil de Arrematante como padrão
        if not hasattr(instance, "arrematante"):
            Arrematante.objects.create(
                user=instance,
                cpf_cnpj='',
                cep='',
                logradouro='',
                numero='',
                complemento='',
                bairro='',
                cidade='',
                estado='',
                pais='',
                telefone_comercial='',
                telefone_celular='',
                tipo_cadastro='PF',  # Tipo padrão Pessoa Física
            )

        # Caso específico: criar perfil de Admin (se necessário, baseado em lógica adicional)
        if not hasattr(instance, "admin"):
            Admin.objects.create(
                user=instance,
                setor='',  # Dados padrão
                telefone='',  # Dados padrão
            )

    # Atualiza o campo user_type, garantindo que o sinal não cause um loop
    user_type = 'default'  # Valor padrão
    if hasattr(instance, "arrematante"):
        user_type = 'arrematante'
    elif hasattr(instance, "admin"):
        user_type = 'admin'

    if instance.user_type != user_type:  # Apenas salva se houver mudança
        instance.user_type = user_type
        instance.save(update_fields=["user_type"])
