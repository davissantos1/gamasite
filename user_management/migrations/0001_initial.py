# Generated by Django 5.1.3 on 2024-12-27 18:12

import django.core.files.storage
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(max_length=100, verbose_name='Setor')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone de Contato')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
            },
        ),
        migrations.CreateModel(
            name='Arrematante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_cnpj', models.CharField(max_length=30)),
                ('cep', models.CharField(max_length=9)),
                ('logradouro', models.CharField(max_length=255)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=255, null=True)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=50)),
                ('pais', models.CharField(max_length=50)),
                ('telefone_comercial', models.CharField(blank=True, max_length=15, null=True)),
                ('telefone_celular', models.CharField(max_length=15)),
                ('tipo_cadastro', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='arrematante', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Arrematante',
                'verbose_name_plural': 'Arrematantes',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(choices=[('RG', 'RG'), ('CNH', 'CNH'), ('PASSAPORTE', 'Passaporte'), ('COMPROVANTE_RESIDENCIA', 'Comprovante de Residência'), ('CONTRATO_SOCIAL', 'Contrato Social'), ('SELFIE', 'Selfie')], max_length=50)),
                ('documento', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\davis\\All\\Projects\\gama\\gamaleiloes\\protected_documents'), upload_to='documentos/')),
                ('data_upload', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('P', 'Pendente'), ('A', 'Aprovado'), ('R', 'Rejeitado')], default='P', max_length=1)),
                ('arrematante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='user_management.arrematante')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
            },
        ),
    ]
